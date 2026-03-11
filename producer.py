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
    # TODO 1: Call sdk.stream_run_metrics(run_id) to get a generator
    #   - Iterate over the generator (it yields Metric objects)
    #   - For each metric, put it on the queue using queue.put(metric)
    #
    # TODO 2: After the stream ends (loop finishes), put SENTINEL on the queue
    #   - This tells consumers "one producer is done"
    #
    # TODO 3: Wrap the entire function body in try/except
    #   - If any exception occurs, increment error_count["count"] using error_lock
    #   - Still put SENTINEL on the queue even if an error occurs (so consumers don't hang)
    #   - Print a warning message with the run_id and error
    pass
