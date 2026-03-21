"""
Application Entry Point Logic
===============================
Fetches active runs and starts the pipeline.
"""

import time
from sdk_do_not_edit import WandbMetricsSDK
from pipeline import run_pipeline
from display import display_active_runs, display_final_summary


def run():
    """Main application logic."""
    sdk = WandbMetricsSDK()

    # Fetch active runs
    runs = sdk.list_active_runs("gpu-training")
    display_active_runs(runs)

    # Extract run IDs
    run_ids = [r.id for r in runs]

    print(f"\nStarting pipeline with {len(run_ids)} producers, 4 consumers...\n")

    start = time.perf_counter()
    snapshot = run_pipeline(sdk, run_ids)
    elapsed = time.perf_counter() - start

    if snapshot:
        display_final_summary(snapshot, elapsed)
    else:
        print("Pipeline returned None.")
