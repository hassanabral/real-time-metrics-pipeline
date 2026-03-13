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
import copy


class MetricsAggregator:
    """
    Thread-safe aggregator that maintains running statistics.

    Multiple consumer threads call record_metric() concurrently,
    and the monitor thread calls get_snapshot() periodically.
    Both must be safe to call from any thread.
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._total_ingested = 0
        self._total_validated = 0
        self._total_invalid = 0
        self._total_errors = 0
        self._metric_to_stats = {}
        self._rid_to_stats = {}

    def record_metric(self, metric: Metric) -> None:
        """
        Record a validated metric. Called from consumer threads.

        Args:
            metric: A validated Metric object
        """
        # obtain lock
        with self._lock:
            # update project metric stats
            self._total_ingested += 1
            self._total_validated += 1

            if metric.metric_name not in self._metric_to_stats:
                self._metric_to_stats[metric.metric_name] = {
                    'count': 0,
                    'sum': 0.0,
                    'min': float('inf'),
                    'max': float('-inf')
                }
            
            metric_stats = self._metric_to_stats[metric.metric_name]
            
            metric_stats['count'] += 1
            metric_stats['sum'] += metric.value
            metric_stats['min'] = min(
                metric_stats['min'], 
                metric.value
            )
            metric_stats['max'] = max(
                metric_stats['max'], 
                metric.value
            )

            # update run stats
            if metric.run_id not in self._rid_to_stats:
                self._rid_to_stats[metric.run_id] = {'count': 0, 'last_step': None}
            run_stats = self._rid_to_stats[metric.run_id]
            run_stats['count'] += 1
            run_stats['last_step'] = metric.step

    def record_invalid(self) -> None:
        """Record that an invalid metric was encountered."""
        # Increment self._total_ingested and self._total_invalid under the lock
        with self._lock:
            self._total_ingested += 1
            self._total_invalid += 1


    def record_error(self) -> None:
        """Record that an error occurred."""
        # Increment self._total_errors under the lock
        with self._lock:
            self._total_errors += 1

    def get_snapshot(self) -> dict:
        """
        Return a snapshot of the current statistics.
        Called from the monitor thread -- must be safe to call concurrently.

        Returns:
            Dict with total_ingested, total_validated, total_invalid,
            total_errors, metrics (with avg computed), per_run
        """
        with self._lock:
            metrics = copy.deepcopy(self._metric_to_stats)
            per_run = copy.deepcopy(self._rid_to_stats)

            for metric_name, stats in metrics.items():
                avg = stats['sum'] / stats['count'] if stats['count'] else 0
                metrics[metric_name]['avg'] = avg

            return {
                'total_ingested': self._total_ingested,
                'total_validated': self._total_validated,
                'total_invalid': self._total_invalid,
                'total_errors': self._total_errors,
                'metrics': metrics,
                'per_run': per_run
            }
