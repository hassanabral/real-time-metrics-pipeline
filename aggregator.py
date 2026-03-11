"""
Thread-Safe Metrics Aggregator
================================
Maintains running statistics for all ingested metrics using locks
to ensure thread safety.

You will implement:
- Thread-safe metric recording using Lock
- Running statistics (count, sum, min, max, avg per metric name)
- Atomic snapshot reads for the monitor thread
"""

import threading
from sdk_do_not_edit import Metric


class MetricsAggregator:
    """
    Thread-safe aggregator that maintains running statistics.

    Multiple consumer threads call record_metric() concurrently,
    and the monitor thread calls get_snapshot() periodically.
    Both must be safe to call from any thread.
    """

    def __init__(self):
        # TODO 7: Initialize the lock and shared state:
        #   - self._lock = threading.Lock()
        #   - self._total_ingested = 0  (count of all metrics recorded)
        #   - self._total_validated = 0  (count of valid metrics)
        #   - self._total_invalid = 0  (count of invalid metrics)
        #   - self._total_errors = 0  (count of errors)
        #   - self._metrics = {}  (dict of metric_name -> {"count": 0, "sum": 0.0, "min": float("inf"), "max": float("-inf")})
        #   - self._per_run = {}  (dict of run_id -> {"count": 0, "last_step": 0})
        pass

    def record_metric(self, metric: Metric) -> None:
        """
        Record a validated metric. Called from consumer threads.

        Args:
            metric: A validated Metric object
        """
        # TODO 8: Acquire self._lock, then:
        #   - Increment self._total_ingested and self._total_validated
        #   - If metric.metric_name not in self._metrics, initialize it
        #   - Update count, sum, min, max for that metric name
        #   - Update per_run tracking (count and last_step)
        #   - Release the lock (use with statement for safety)
        pass

    def record_invalid(self) -> None:
        """Record that an invalid metric was encountered."""
        # Increment self._total_ingested and self._total_invalid under the lock
        pass

    def record_error(self) -> None:
        """Record that an error occurred."""
        # Increment self._total_errors under the lock
        pass

    def get_snapshot(self) -> dict:
        """
        Return a snapshot of the current statistics.
        Called from the monitor thread -- must be safe to call concurrently.

        Returns:
            Dict with total_ingested, total_validated, total_invalid,
            total_errors, metrics (with avg computed), per_run
        """
        # TODO 9: Acquire self._lock, then:
        #   - Create a deep copy of all state
        #   - For each metric in the copy, compute avg = sum / count (handle count=0)
        #   - Return the snapshot dict (see display.py for expected shape)
        #   - Release the lock
        pass
