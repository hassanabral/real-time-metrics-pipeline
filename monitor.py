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
    # TODO 10: Loop until stop_event is set:
    #   - Call aggregator.get_snapshot()
    #   - Pass the snapshot to display_fn(snapshot)
    #   - Use stop_event.wait(interval) instead of time.sleep(interval)
    #     (this allows immediate wake-up when stop_event is set)
    #
    # TODO 11: After the loop exits (stop_event is set):
    #   - Do one final snapshot + display to show final stats
    pass
