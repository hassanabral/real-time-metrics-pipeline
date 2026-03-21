# Real-Time Metrics Pipeline

**Practice Project 2** | Medium Difficulty | ~45-55 minutes

A producer-consumer pipeline that ingests live metrics from multiple ML experiments. Producer threads stream metrics into a shared queue, consumer threads validate and process them, and a stats aggregator maintains running statistics with thread-safe access. A monitor thread periodically prints live stats.

---

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

When you first run it, you'll see the active runs table and the pipeline will stream and process metrics in real time.

---

## Project Structure

```
concurrency-project-2/
    main.py                          # Entry point (pre-built)
    app.py                           # Application logic         <-- MODIFY
    pipeline.py                      # Pipeline orchestrator      <-- MODIFY
    producer.py                      # Metric producers           <-- MODIFY
    consumer.py                      # Metric consumers           <-- MODIFY
    aggregator.py                    # Thread-safe aggregator     <-- MODIFY
    monitor.py                       # Live stats monitor         <-- MODIFY
    display.py                       # Rich display helpers (pre-built)
    requirements.txt
    sdk_do_not_edit/
        __init__.py
        wandb_metrics_sdk.py         # Mocked W&B SDK (DO NOT EDIT)
    README.md
```

---

## What You're Building

```
  Producer-1 ----\                          /---- Consumer-1 ---\
  Producer-2 -----\                        /---- Consumer-2 -----\
  Producer-3 ------+---> [ Queue ] ---+---+---- Consumer-3 ------+--> Aggregator
  Producer-4 ------+    (maxsize=100)  |   \---- Consumer-4 ---/        |
  Producer-5 -----/                    |                                |
  Producer-6 ----/                     |                                v
                                       |                          Monitor Thread
                                   Sentinel                     (periodic stats)
                                   Signaling
```

Each **producer** streams metrics from one ML experiment run via the SDK. Metrics flow through a bounded **Queue** to **consumers**, which validate each metric (respecting the SDK's rate limit via a **Semaphore**) and record valid ones in a thread-safe **Aggregator**. A **monitor** thread periodically reads a snapshot from the aggregator and displays live stats. An **Event** coordinates graceful shutdown.

---

## Concepts Covered

| Concept | Where It's Used |
|---|---|
| `threading.Thread` | All files -- producers, consumers, monitor |
| `queue.Queue` | Shared buffer between producers and consumers |
| `threading.Lock` | Aggregator state protection, error counting |
| `threading.Semaphore` | Rate-limiting SDK validate calls |
| `threading.Event` | Graceful shutdown signaling |
| Sentinel values | Producers signal completion via `SENTINEL = None` |
| Producer-Consumer pattern | Core architecture |
| Graceful shutdown | Coordinated thread termination |

---

## Files To Modify

### `aggregator.py`
The data store that everything writes to and reads from. Initializes the lock and shared state, implements `record_metric()` and `get_snapshot()`.

### `producer.py`
Streams metrics from the SDK into the queue. Iterates over `sdk.stream_run_metrics(run_id)`, puts each metric on the queue, and sends a `SENTINEL` when the stream ends.
![alt text](image-1.png)

### `consumer.py`
Pulls from the queue, validates, and records. Handles SENTINEL to track producer completion, validates metrics using the semaphore for rate limiting, and catches exceptions gracefully.
![alt text](image.png)

### `monitor.py`
Periodically displays live stats by calling `get_snapshot()` and `display_fn()` until `stop_event` is set, with one final display after shutdown.

### `pipeline.py`
Wires everything together: creates the semaphore, starts producer threads (one per run), starts 4 consumer threads, starts the monitor thread, and joins threads in correct order.

### `app.py`
Entry point that fetches active runs and starts the pipeline.

---

## SDK Reference

### `WandbMetricsSDK`

| Method | Description |
|---|---|
| `list_active_runs(project_id)` | Returns `list[ActiveRun]` for a project. ~100ms delay. |
| `stream_run_metrics(run_id)` | Generator yielding `Metric` objects (8-15 per run, 50-200ms between). |
| `validate_metric(metric)` | Returns `bool`. **Rate limited: max 20 calls/sec.** Raises `RateLimitError`. |

### Data Types

```python
@dataclass
class ActiveRun:
    id: str
    name: str
    model_type: str
    started_at: float
    status: str = "running"

@dataclass
class Metric:
    run_id: str
    step: int
    metric_name: str   # "loss", "accuracy", "learning_rate", "gpu_utilization", "memory_usage"
    value: float
    timestamp: float
```

### `RateLimitError`
Raised by `validate_metric()` when called more than 20 times within one second. Your consumer must handle this (e.g., sleep briefly and retry).

---

## Suggested Implementation Order

```
aggregator.py  -->  producer.py  -->  consumer.py  -->  monitor.py  -->  pipeline.py  -->  app.py
```

Start with the aggregator because it has no dependencies and you can mentally verify it. Then producers (simple SDK iteration), consumers (the trickiest -- rate limiting and sentinel handling), monitor (straightforward loop), and finally the pipeline orchestrator that wires it all together.

---

## Tips

1. **Always send the sentinel.** If a producer crashes without putting `SENTINEL` on the queue, consumers will wait forever. Use `try/finally` to guarantee it.

2. **Use `with self._lock:` instead of manual acquire/release.** The `with` statement guarantees the lock is released even if an exception occurs.

3. **The semaphore value should be less than 20.** The SDK allows 20 calls/sec. Using a semaphore of 15 gives headroom. If you use exactly 20, timing jitter can still trigger `RateLimitError`.

4. **Use `stop_event.wait(interval)` not `time.sleep(interval)`.** The `wait()` method returns immediately when the event is set, allowing faster shutdown.

5. **Use `queue.get(timeout=0.5)` not `queue.get()`.** Without a timeout, consumers block forever if producers are done but they missed the sentinel.

6. **Handle `queue.Empty` exception.** When the timeout expires, `queue.get()` raises `queue.Empty`. Just continue the loop.

7. **Join threads in order: producers first, then wait for stop_event, then consumers, then monitor.** This ensures clean shutdown without deadlocks.

8. **The aggregator's `get_snapshot()` must return a deep copy.** If you return references to the internal dicts, the monitor thread might read stale or partially-updated data.

---

## Expected Output

When fully implemented, you should see:
- A table of 6 active experiment runs
- Periodic pipeline stats updates (every 0.5s)
- A final summary showing ~50-90 total metrics processed across all runs
- Pipeline completes in ~3-5 seconds
- Throughput of ~15-30 metrics/sec
