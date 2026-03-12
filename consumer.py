"""
Metric Consumers
=================
Consumer threads that pull metrics from the Queue, validate them, and
pass valid metrics to the aggregator.

You will implement:
- A consumer function that processes metrics from the queue
- Rate-limited validation using a Semaphore
- Proper shutdown when all producers are done
"""

import threading
from queue import Queue
from sdk_do_not_edit import WandbMetricsSDK, Metric, RateLimitError
from producer import SENTINEL
import time


def consume_metrics(
    sdk: WandbMetricsSDK,
    queue: Queue,
    aggregator,  # MetricsAggregator instance
    semaphore: threading.Semaphore,
    producers_remaining: dict,
    producers_lock: threading.Lock,
    stop_event: threading.Event,
) -> None:
    """
    Consumer function -- runs in its own thread.

    Pulls metrics from the shared queue, validates them using the SDK
    (rate-limited via semaphore), and passes valid metrics to the aggregator.

    Args:
        sdk: The SDK client
        queue: Shared queue to pull metrics from
        aggregator: MetricsAggregator instance (has record_metric and record_invalid methods)
        semaphore: Semaphore limiting concurrent validate_metric calls (max 15 to stay under 20/sec limit)
        producers_remaining: Shared dict {"count": int} tracking active producers
        producers_lock: Lock protecting producers_remaining
        stop_event: Event that signals "time to stop"
    """
    # TODO 4: Loop until stop_event is set:
    #   - Use queue.get(timeout=0.5) to pull an item (use try/except queue.Empty to handle timeout)
    #   - If the item is SENTINEL:
    #       - Decrement producers_remaining["count"] under producers_lock
    #       - If producers_remaining["count"] == 0, set stop_event (all producers done)
    #       - Continue to next iteration
    #   - The item is a Metric object -- proceed to validate it
    #
    # TODO 5: Validate the metric using rate limiting:
    #   - Acquire the semaphore (semaphore.acquire())
    #   - Try: call sdk.validate_metric(metric)
    #   - If RateLimitError: sleep 0.1 seconds and retry once
    #   - Finally: release the semaphore (semaphore.release())
    #   - If valid: call aggregator.record_metric(metric)
    #   - If invalid: call aggregator.record_invalid()
    #
    # TODO 6: Handle any other exceptions gracefully
    #   - Print a warning and continue processing (don't crash the consumer)
    
    """Thinking
    - pull metrics from the queue
    - validate each metric
    - pass the valid ones to the aggregator
    """

    # pull metrics from the queue until the stop signal fires

    # while stop signal is not set, process the next metric from queue
    while not stop_event.is_set():
        # get metric from queue
        try:
            metric = queue.get(timeout=0.5) 
        except queue.Empty as e:
            # continue if queue is empty
            continue

        # if we see a SENTINEL node
        if metric is SENTINEL:
            # decrement producer count, and send stop signal if count is 0
            with producers_lock:
                producers_remaining['count'] -= 1
                if producers_remaining['count'] == 0:
                    stop_event.set()
            continue
        # for metric node
        try:
            # validate metric (while respecting rate limit using semaphore)
            with semaphore:
                try:
                    is_valid = sdk.validate_metric(metric)
                except RateLimitError as e:
                    # retry once after 0.1 sec if rate limited
                    time.sleep(0.1)
                    is_valid = sdk.validate_metric(metric)
            # call aggregator to record valid and invalid metrics
            if not is_valid:
                aggregator.record_invalid()
            else:
                aggregator.record_metric(metric)
        except Exception as e:
            print("Error consuming metric", e)
            aggregator.record_error()
            # coninue so that we don't crash the thread for one failed metric
            continue
        
