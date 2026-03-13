"""
Pipeline Monitor
==================
Monitor thread that periodically displays live pipeline statistics.

You will implement:
- A monitor loop that reads from the aggregator periodically
- Graceful shutdown using an Event
"""

import threading
import time


def run_monitor(
    aggregator,  # MetricsAggregator instance
    stop_event: threading.Event,
    display_fn,  # callable that takes a snapshot dict
    interval: float = 0.5,
) -> None:
    """
    Monitor function -- runs in its own thread.

    Periodically calls aggregator.get_snapshot() and passes the result
    to display_fn for rendering. Stops when stop_event is set.

    Args:
        aggregator: MetricsAggregator instance
        stop_event: Event that signals "time to stop"
        display_fn: Function to call with each snapshot
        interval: Seconds between updates (default 0.5)
    """
    while not stop_event.is_set():
        # call aggregator get snapshot with 0.5 timeout
        try:
            snapshot = aggregator.get_snapshot()
            display_fn(snapshot)

            # periodic call every 0.5 sec
            stop_event.wait(interval)
        except Exception as e:
            print("Error runing monitor", e)
            continue

    # one last snapshot after exiting
    try:
        snapshot = aggregator.get_snapshot()
        display_fn(snapshot)
    except Exception as e:
        print("Error fetching and displaying snapshot", e)
    
