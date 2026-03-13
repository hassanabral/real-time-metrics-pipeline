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


MAX_SEMAPHORES = 2 # to stay under 20/s
MONITOR_INTERVAL = 0.5

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

    # Return final snapshot
    # return aggregator.get_snapshot()
    # Shared resources (pre-created)
    queue = Queue(maxsize=100)
    aggregator = MetricsAggregator()
    stop_event = threading.Event()
    error_count = {"count": 0}
    error_lock = threading.Lock()
    producers_remaining = {"count": len(run_ids)}
    producers_lock = threading.Lock()

    # create producer threads for runs
    pthreads = []
    for run_id in run_ids:
        pthread = threading.Thread(target=produce_metrics, args=(
            sdk,
            run_id,
            queue,
            error_count,
            error_lock
        ),
        daemon=True)
        pthreads.append(pthread)
    
    # create consumer threads
    validate_semaphore = threading.Semaphore(MAX_SEMAPHORES)
    cthreads = []
    for i in range(4):
        cthread = threading.Thread(target=consume_metrics, args=(
            sdk,
            queue,
            aggregator,
            validate_semaphore,
            producers_remaining,
            producers_lock,
            stop_event
        ), daemon=True)
        cthreads.append(cthread)
    
    # setup monitor thread
    mthread = threading.Thread(target=run_monitor, 
        args=(
            aggregator, 
            stop_event, 
            display_pipeline_stats,
            MONITOR_INTERVAL
    ), daemon=True)

    # start threads
    for pthread in pthreads:
        pthread.start()
    
    for cthread in cthreads:
        cthread.start()
    
    mthread.start()

    # join threads
    for pthread in pthreads:
        pthread.join()
    
    stop_event.wait(timeout=30)

    for cthread in cthreads:
        cthread.join(timeout=30)
    
    stop_event.set()
    
    mthread.join(timeout=30)

    # return final snapshot
    snapshot = aggregator.get_snapshot()
    return snapshot
