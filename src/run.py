# src/run.py
from __future__ import annotations
import argparse
import logging
from src.orchestrator import run_pipeline  # type: ignore

LOG = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", default="Analyze ROAS drop")
    parser.add_argument("--cfg", type=str, default=None, help="Optional config file (json)")
    args = parser.parse_args()

    # run pipeline - expected to return a summary dict
    summary = run_pipeline(args.query, cfg=args.cfg or {})
    LOG.info("=== RUN SUMMARY ===")
    LOG.info(summary)


if __name__ == "__main__":
    main()
