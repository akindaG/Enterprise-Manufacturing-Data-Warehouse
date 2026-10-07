"""Incremental fact loading with historical surrogate-key resolution."""

from __future__ import annotations

from datetime import date

import pandas as pd
from sqlalchemy import text


def dimension_key(connection, table: str, key_col: str, natural_col: str, value) -> int:
    result = connection.execute(
        text(f"SELECT {key_col} FROM {table} WHERE {natural_col}=:value"),
        {"value": value},
    ).scalar_one_or_none()
    if result is None:
        raise ValueError(f"Dimension lookup failed: {table}.{natural_col}={value}")
    return int(result)


def machine_key_for_date(connection, machine_id: str, production_date: date) -> int:
    """Resolve the machine version valid on the production business date."""
    result = connection.execute(
        text(
            """
            SELECT machine_key
            FROM dim_machine
            WHERE machine_id=:machine_id
              AND effective_date <= :production_date
              AND expiry_date >= :production_date
            ORDER BY effective_date DESC
            LIMIT 1
            """
        ),
        {"machine_id": machine_id, "production_date": production_date},
    ).scalar_one_or_none()
    if result is None:
        raise ValueError(f"No SCD version for machine {machine_id} on {production_date}")
    return int(result)


def load_facts(connection, production: pd.DataFrame) -> int:
    """Insert unseen production events. Production_ID is the idempotency key."""
    inserted = 0

    for row in production.to_dict("records"):
        production_date = pd.to_datetime(row["production_date"]).date()
        params = {
            "production_id": str(row["production_id"]),
            "date_key": int(production_date.strftime("%Y%m%d")),
            "product_key": dimension_key(connection, "dim_product", "product_key", "product_id", row["product_id"]),
            "machine_key": machine_key_for_date(connection, row["machine_id"], production_date),
            "factory_key": dimension_key(connection, "dim_factory", "factory_key", "factory_id", row["factory_id"]),
            "employee_key": dimension_key(connection, "dim_employee", "employee_key", "employee_id", row["employee_id"]),
            "shift_key": dimension_key(connection, "dim_shift", "shift_key", "shift_id", row["shift_id"]),
            "quantity_produced": int(row["quantity"]),
            "production_cost": float(row["production_cost"]),
            "production_time": int(row["production_time"]),
            "defect_count": int(row["defect_count"]),
        }

        result = connection.execute(
            text(
                """
                INSERT INTO fact_production(
                    production_id, date_key, product_key, machine_key, factory_key,
                    employee_key, shift_key, quantity_produced, production_cost,
                    production_time, defect_count
                ) VALUES (
                    :production_id, :date_key, :product_key, :machine_key, :factory_key,
                    :employee_key, :shift_key, :quantity_produced, :production_cost,
                    :production_time, :defect_count
                )
                ON CONFLICT (production_id) DO NOTHING
                RETURNING production_key
                """
            ),
            params,
        ).scalar_one_or_none()
        if result is not None:
            inserted += 1

    return inserted
