"""Transactional orchestration for the Enterprise Manufacturing Data Platform."""

from __future__ import annotations

from datetime import date, datetime
from pathlib import Path

from sqlalchemy import create_engine, text

from etl_pipeline.database import ensure_run_log
from etl_pipeline.dimension_loader import (
    load_date_dimension,
    load_machine_scd2,
    upsert_type1_dimension,
)
from etl_pipeline.extract import extract_source_state
from etl_pipeline.fact_loader import load_facts
from etl_pipeline.staging import load_to_staging
from etl_pipeline.transform import clean_source_state
from etl_pipeline.validation import validate_sources


def run_pipeline(source_dir: Path, run_date: date, database_url: str) -> dict[str, int]:
    """Execute one atomic snapshot-to-warehouse load."""
    raw = extract_source_state(source_dir)
    data = clean_source_state(raw)
    validate_sources(data, run_date)

    engine = create_engine(database_url, pool_pre_ping=True)
    with engine.begin() as connection:
        ensure_run_log(connection)
        load_to_staging(data, connection)
        load_date_dimension(connection, data["production"])

        upsert_type1_dimension(
            connection, data["product"], "dim_product", "product_id",
            ["product_name", "category", "unit_cost"],
        )
        upsert_type1_dimension(
            connection, data["factory"], "dim_factory", "factory_id",
            ["factory_name", "location", "capacity"],
        )
        upsert_type1_dimension(
            connection, data["employee"], "dim_employee", "employee_id",
            ["employee_name", "department", "role"],
        )
        upsert_type1_dimension(
            connection, data["shift"], "dim_shift", "shift_id",
            ["shift_name", "start_time", "end_time"],
        )

        machine_versions = load_machine_scd2(connection, data["machine"], run_date)
        facts_inserted = load_facts(connection, data["production"])

        connection.execute(
            text(
                """
                INSERT INTO etl_run_log(
                    executed_at, run_date, source_dir, status,
                    facts_inserted, machine_versions_created
                ) VALUES (:executed_at, :run_date, :source_dir, 'SUCCESS', :facts, :machines)
                """
            ),
            {
                "executed_at": datetime.now(),
                "run_date": run_date,
                "source_dir": str(source_dir),
                "facts": facts_inserted,
                "machines": machine_versions,
            },
        )

    return {"facts_inserted": facts_inserted, "machine_versions_created": machine_versions}
