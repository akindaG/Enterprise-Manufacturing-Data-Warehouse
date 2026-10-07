"""Dimension loading, including date-aware SCD Type 2 handling."""

from __future__ import annotations

from datetime import date, timedelta

import pandas as pd
from sqlalchemy import text

from etl_pipeline.scd_type2 import has_tracked_change


def load_date_dimension(connection, production: pd.DataFrame) -> None:
    dates = pd.to_datetime(production["production_date"], errors="raise").dt.date.unique()
    for production_date in dates:
        connection.execute(
            text(
                """
                INSERT INTO dim_date(date_key, full_date, day, month, quarter, year)
                VALUES (:date_key, :full_date, :day, :month, :quarter, :year)
                ON CONFLICT (date_key) DO NOTHING
                """
            ),
            {
                "date_key": int(production_date.strftime("%Y%m%d")),
                "full_date": production_date,
                "day": production_date.day,
                "month": production_date.month,
                "quarter": ((production_date.month - 1) // 3) + 1,
                "year": production_date.year,
            },
        )


def upsert_type1_dimension(connection, df, table: str, natural_col: str, attributes: list[str]) -> None:
    """Upsert Type 1 dimensions while letting PostgreSQL generate surrogate keys."""
    columns = [natural_col] + attributes
    assignments = ", ".join(f"{col}=EXCLUDED.{col}" for col in attributes)
    statement = text(
        f"INSERT INTO {table} ({', '.join(columns)}) "
        f"VALUES ({', '.join(':' + col for col in columns)}) "
        f"ON CONFLICT ({natural_col}) DO UPDATE SET {assignments}"
    )
    for row in df.to_dict("records"):
        connection.execute(statement, {column: row[column] for column in columns})


def load_machine_scd2(connection, machines: pd.DataFrame, run_date: date) -> int:
    """Create/expire machine versions only when tracked attributes change."""
    versions_created = 0

    for row in machines.to_dict("records"):
        current = connection.execute(
            text(
                """
                SELECT machine_key, machine_name, machine_type, factory_id, machine_status
                FROM dim_machine
                WHERE machine_id=:machine_id AND is_current=TRUE
                """
            ),
            {"machine_id": row["machine_id"]},
        ).mappings().first()

        old_record = None
        if current:
            old_record = {
                "machine_name": current["machine_name"],
                "machine_type": current["machine_type"],
                "factory_id": current["factory_id"],
                "status": current["machine_status"],
            }

        if old_record is not None and not has_tracked_change(old_record, row):
            continue

        if current:
            connection.execute(
                text(
                    """
                    UPDATE dim_machine
                    SET expiry_date=:expiry_date, is_current=FALSE
                    WHERE machine_key=:machine_key
                    """
                ),
                {
                    "expiry_date": run_date - timedelta(days=1),
                    "machine_key": current["machine_key"],
                },
            )

        connection.execute(
            text(
                """
                INSERT INTO dim_machine(
                    machine_id, machine_name, machine_type, factory_id,
                    machine_status, effective_date, expiry_date, is_current
                ) VALUES (
                    :machine_id, :machine_name, :machine_type, :factory_id,
                    :machine_status, :effective_date, DATE '9999-12-31', TRUE
                )
                """
            ),
            {
                "machine_id": row["machine_id"],
                "machine_name": row["machine_name"],
                "machine_type": row["machine_type"],
                "factory_id": row["factory_id"],
                "machine_status": row["status"],
                "effective_date": run_date,
            },
        )
        versions_created += 1

    return versions_created
