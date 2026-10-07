"""CLI entrypoint for one manufacturing warehouse ETL run."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path

from etl_pipeline.config import database_url_from_environment
from etl_pipeline.pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Enterprise Manufacturing DW ETL")
    parser.add_argument("--source-dir", required=True, help="Snapshot directory containing source CSV files")
    parser.add_argument("--run-date", required=True, help="Business effective date in YYYY-MM-DD format")
    args = parser.parse_args()

    run_date = date.fromisoformat(args.run_date)
    result = run_pipeline(
        Path(args.source_dir),
        run_date,
        database_url_from_environment(),
    )

    print(
        "ETL SUCCESS | "
        f"run_date={run_date} | "
        f"facts_inserted={result['facts_inserted']} | "
        f"machine_versions_created={result['machine_versions_created']}"
    )


if __name__ == "__main__":
    main()
