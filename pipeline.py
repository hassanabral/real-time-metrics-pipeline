"""
Pipeline Orchestrator
======================
Wires together producers, consumers, aggregator, and monitor.

You will implement:
- Starting the right number of producer and consumer threads
- Proper synchronization and shutdown sequencing
"""

import threading
from queue import Queue
from sdk_do_not_edit import WandbMetricsSDK
from producer import produce_metrics
from consumer import consume_metrics
from aggregator import MetricsAggregator
from monitor import run_monitor
from display import display_pipeline_stats


def run_pipeline(sdk: WandbMetricsSDK, run_ids: list[str]) -> dict:
    """
    Run the complete metrics pipeline.

    Creates and coordinates:
    - One producer thread per run
    - 4 consumer threads
    - 1 monitor thread
    - Shared queue, aggregator, semaphore, and synchronization primitives

    Args:
        sdk: The SDK client
        run_ids: List of run IDs to stream metrics from

    Returns:
        Final snapshot dict from the aggregator
    """
    # Shared resources (pre-created)
    queue = Queue(maxsize=100)
    aggregator = MetricsAggregator()
    stop_event = threading.Event()
    error_count = {"count": 0}
    error_lock = threading.Lock()
    producers_remaining = {"count": len(run_ids)}
    producers_lock = threading.Lock()

    # TODO 12: Create a Semaphore with value 15 (to stay under the SDK's 20/sec rate limit)
    #   semaphore = threading.Semaphore(15)

    # TODO 13: Start producer threads -- one per run_id
    #   - Create a threading.Thread for each run_id, targeting produce_metrics
    #   - Pass: sdk, run_id, queue, error_count, error_lock
    #   - Set daemon=True on each thread
    #   - Start each thread
    #   - Collect threads in a list

    # TODO 14: Start consumer threads -- 4 workers
    #   - Create 4 threading.Thread instances, targeting consume_metrics
    #   - Pass: sdk, queue, aggregator, semaphore, producers_remaining, producers_lock, stop_event
    #   - Set daemon=True
    #   - Start each thread
    #   - Collect threads in a list

    # TODO 15: Start 1 monitor thread
    #   - Create a threading.Thread targeting run_monitor
    #   - Pass: aggregator, stop_event, display_pipeline_stats, interval=0.5
    #   - Set daemon=True
    #   - Start the thread

    # TODO 16: Wait for completion
    #   - Join all producer threads (they finish when their stream ends)
    #   - Wait for stop_event to be set (consumers set it when all producers are done)
    #   - Or use stop_event.wait(timeout=30) as a safety timeout
    #   - Join all consumer threads with a timeout
    #   - Set stop_event if not already set (to stop the monitor)
    #   - Join the monitor thread

    # Return final snapshot
    # return aggregator.get_snapshot()
    pass
