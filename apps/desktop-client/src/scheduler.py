"""
scheduler.py
~~~~~~~~~~~~
Background task orchestration for the Tally-Sync Desktop Client.

Uses APScheduler to trigger `run_full_sync` from tally_client.py
at a configurable interval (default: every 60 minutes).

Run:
    python scheduler.py               # live mode (every 60 min)
    python scheduler.py --interval 5  # every 5 minutes (testing)
    python scheduler.py --run-once    # single immediate sync, then exit
"""

from __future__ import annotations

import argparse
import logging
import os
import sys
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger

sys.path.insert(0, os.path.dirname(__file__))
from tally_client import run_full_sync  # noqa: E402  (after path fixup)

log = logging.getLogger("scheduler")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
)

FROM_DATE: str = os.getenv("SYNC_FROM_DATE", "20240401")
TO_DATE:   str = os.getenv("SYNC_TO_DATE",   "20250331")


def _sync_job() -> None:
    """Scheduled job: runs the full sync cycle; logs but never raises."""
    try:
        run_full_sync(FROM_DATE, TO_DATE)
    except Exception as exc:  # pragma: no cover
        log.error("Sync job raised an unexpected error: %s", exc, exc_info=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tally Sync Scheduler")
    parser.add_argument("--interval", type=int, default=60, help="Sync interval in minutes.")
    parser.add_argument("--run-once", action="store_true", help="Run once immediately and exit.")
    args = parser.parse_args()

    if args.run_once:
        log.info("Running a single sync cycle now …")
        _sync_job()
        return

    scheduler = BlockingScheduler(timezone="Asia/Kolkata")
    scheduler.add_job(
        _sync_job,
        trigger=IntervalTrigger(minutes=args.interval),
        id="tally_full_sync",
        name="Tally Full Sync",
        max_instances=1,          # prevent overlap if a cycle takes too long
        replace_existing=True,
        next_run_time=__import__("datetime").datetime.now(),  # run immediately on start
    )

    log.info("Scheduler started – syncing every %d minute(s). Press Ctrl+C to stop.", args.interval)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        log.info("Scheduler stopped.")


if __name__ == "__main__":
    main()

