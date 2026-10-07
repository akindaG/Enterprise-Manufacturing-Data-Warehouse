"""Fail-fast source data quality and referential-integrity checks."""

from __future__ import annotations

from datetime import date

import pandas as pd

from etl_pipeline.config import BUSINESS_KEYS, REQUIRED_COLUMNS


def validate_sources(data: dict[str, pd.DataFrame], run_date: date) -> None:
    for name, required in REQUIRED_COLUMNS.items():
        missing = required.difference(data[name].columns)
        if missing:
            raise ValueError(f"{name}: missing required columns {sorted(missing)}")
        if data[name].empty:
            raise ValueError(f"{name}: source dataset is empty")

        key = BUSINESS_KEYS[name]
        if data[name][key].isna().any():
            raise ValueError(f"{name}: null business key detected in {key}")
        if data[name][key].duplicated().any():
            duplicate_keys = data[name].loc[data[name][key].duplicated(), key].tolist()
            raise ValueError(f"{name}: duplicate business keys detected: {duplicate_keys}")

    production = data["production"].copy()
    for column in ["quantity", "production_time", "production_cost", "defect_count"]:
        production[column] = pd.to_numeric(production[column], errors="raise")
        if (production[column] < 0).any():
            raise ValueError(f"production: negative values detected in {column}")

    if (production["defect_count"] > production["quantity"]).any():
        raise ValueError("production: defect_count cannot exceed quantity")

    production_dates = pd.to_datetime(production["production_date"], errors="raise").dt.date
    if any(production_date > run_date for production_date in production_dates):
        raise ValueError("production: source contains a production_date after the ETL run_date")

    reference_checks = {
        "product_id": set(data["product"]["product_id"]),
        "machine_id": set(data["machine"]["machine_id"]),
        "factory_id": set(data["factory"]["factory_id"]),
        "employee_id": set(data["employee"]["employee_id"]),
        "shift_id": set(data["shift"]["shift_id"]),
    }
    for column, valid_values in reference_checks.items():
        invalid = set(production[column]).difference(valid_values)
        if invalid:
            raise ValueError(f"production: unknown {column} values {sorted(invalid)}")

    machine_factories = dict(zip(data["machine"]["machine_id"], data["machine"]["factory_id"]))
    inconsistent = production[
        production.apply(
            lambda row: machine_factories[row["machine_id"]] != row["factory_id"], axis=1
        )
    ]
    if not inconsistent.empty:
        raise ValueError(
            "production: factory_id does not match the machine assignment for "
            f"production IDs {inconsistent['production_id'].tolist()}"
        )
