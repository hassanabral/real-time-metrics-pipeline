"""
Metric Producers
=================
Producer threads that stream metrics from the SDK into a shared Queue.

You will implement:
- A producer function that reads from the SDK's metric stream
- Proper sentinel value signaling when a producer is done
- Error handling for SDK failures within the producer thread
"""

import threading
from queue import Queue
from sdk_do_not_edit import WandbMetricsSDK, Metric

# Sentinel value to signal "this producer is done"
SENTINEL = None


def produce_metrics(
    sdk: WandbMetricsSDK,
    run_id: str,
    queue: Queue,
    error_count: dict,
    error_lock: threading.Lock,
) -> None:
    """
    Producer function -- runs in its own thread.

    Streams metrics from sdk.stream_run_metrics(run_id) and puts each
    metric on the shared queue. When the stream ends, puts SENTINEL on
    the queue to signal completion.

    Args:
        sdk: The SDK client
        run_id: ID of the run to stream metrics from
        queue: Shared queue to put metrics on
        error_count: Shared dict {"count": int} for tracking errors
        error_lock: Lock protecting error_count
    """
    try:
        for metric in sdk.stream_run_metrics(run_id):
            queue.put(metric)
    except Exception as e:
        print(f"Error streaming metric for run {run_id}", e)
        # increment error count with lock
        with error_lock:
            error_count['count'] += 1
    finally:
        queue.put(SENTINEL)
