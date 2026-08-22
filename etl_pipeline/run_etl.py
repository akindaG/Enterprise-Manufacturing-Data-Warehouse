"""End-to-end ETL orchestrator for the Enterprise Manufacturing Data Warehouse.

Run 1:
    python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
Run 2:
    python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15

Set DATABASE_URL for PostgreSQL, for example:
postgresql+psycopg2://postgres:postgres@localhost:5432/manufacturing_dw
"""

from __future__ import annotations

import argparse
import os
from datetime import date, datetime, timedelta
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

FILES = {
    "product": "products.csv",
    "factory": "factories.csv",
    "machine": "machines.csv",
    "employee": "employees.csv",
    "shift": "shifts.csv",
    "production": "production_orders.csv",
}

REQUIRED_COLUMNS = {
    "product": {"product_id", "product_name", "category", "unit_cost"},
    "factory": {"factory_id", "factory_name", "location", "capacity"},
    "machine": {"machine_id", "machine_name", "machine_type", "factory_id", "status"},
    "employee": {"employee_id", "employee_name", "department", "role"},
    "shift": {"shift_id", "shift_name", "start_time", "end_time"},
    "production": {
        "production_id",
        "product_id",
        "machine_id",
        "factory_id",
        "employee_id",
        "shift_id",
        "production_date",
        "quantity",
        "production_time",
        "production_cost",
        "defect_count",
    },
}

BUSINESS_KEYS = {
    "product": "product_id",
    "factory": "factory_id",
    "machine": "machine_id",
    "employee": "employee_id",
    "shift": "shift_id",
    "production": "production_id",
}


def extract(source_dir: Path) -> dict[str, pd.DataFrame]:
    """Read all required source CSV files from one reproducible source state."""
    data: dict[str, pd.DataFrame] = {}
    for name, filename in FILES.items():
        path = source_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing source file: {path}")
        data[name] = pd.read_csv(path)
    return data


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names, trim text fields and remove exact duplicate rows."""
    df = df.copy()
    df.columns = [c.strip().lower() for c in df.columns]
    df = df.drop_duplicates()
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].map(lambda x: x.strip() if isinstance(x, str) else x)
    return df


def validate_sources(data: dict[str, pd.DataFrame]) -> None:
    """Fail fast when a source state violates required data-quality rules."""
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
            duplicates = data[name].loc[data[name][key].duplicated(), key].tolist()
            raise ValueError(f"{name}: duplicate business keys detected: {duplicates}")

    production = data["production"].copy()
    numeric_columns = ["quantity", "production_time", "production_cost", "defect_count"]
    for column in numeric_columns:
        production[column] = pd.to_numeric(production[column], errors="raise")
        if (production[column] < 0).any():
            raise ValueError(f"production: negative values detected in {column}")

    if (production["defect_count"] > production["quantity"]).any():
        raise ValueError("production: defect_count cannot exceed quantity")

    pd.to_datetime(production["production_date"], errors="raise")


def stage(data: dict[str, pd.DataFrame], connection) -> None:
    """Load cleaned source states into reproducible staging tables."""
    for name, df in data.items():
        df.to_sql(f"stg_{name}", connection, if_exists="replace", index=False)


def next_key(connection, table: str, key_col: str) -> int:
    """Generate the next integer warehouse surrogate key."""
    return int(
        connection.execute(
            text(f"SELECT COALESCE(MAX({key_col}), 0) + 1 FROM {table}")
        ).scalar_one()
    )


def ensure_run_log(connection) -> None:
    """Create an auditable ETL execution log if it does not already exist."""
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS etl_run_log (
                run_id SERIAL PRIMARY KEY,
                executed_at TIMESTAMP NOT NULL,
                run_date DATE NOT NULL,
                source_dir VARCHAR(255) NOT NULL,
                status VARCHAR(20) NOT NULL,
                facts_inserted INT NOT NULL DEFAULT 0,
                machine_versions_created INT NOT NULL DEFAULT 0
            )
            """
        )
    )


def load_date_dimension(connection, production: pd.DataFrame) -> None:
    dates = pd.to_datetime(production["production_date"], errors="raise").dt.date.unique()
    for d in dates:
        key = int(d.strftime("%Y%m%d"))
        exists = connection.execute(
            text("SELECT 1 FROM dim_date WHERE date_key=:k"), {"k": key}
        ).first()
        if exists:
            continue

        connection.execute(
            text(
                """
                INSERT INTO dim_date(date_key, full_date, day, month, quarter, year)
                VALUES (:k, :d, :day, :month, :quarter, :year)
                """
            ),
            {
                "k": key,
                "d": d,
                "day": d.day,
                "month": d.month,
                "quarter": ((d.month - 1) // 3) + 1,
                "year": d.year,
            },
        )


def load_simple_dimension(connection, df, table, key_col, natural_col, attributes) -> None:
    """Load new members and apply Type 1 updates to non-historical dimensions."""
    for row in df.to_dict("records"):
        existing = connection.execute(
            text(f"SELECT {key_col} FROM {table} WHERE {natural_col}=:nk"),
            {"nk": row[natural_col]},
        ).scalar_one_or_none()

        if existing is None:
            key = next_key(connection, table, key_col)
            columns = [key_col, natural_col] + attributes
            params = {key_col: key, natural_col: row[natural_col]}
            params.update({a: row[a] for a in attributes})
            connection.execute(
                text(
                    f"INSERT INTO {table} ({', '.join(columns)}) "
                    f"VALUES ({', '.join(':' + c for c in columns)})"
                ),
                params,
            )
            continue

        assignments = ", ".join(f"{attribute}=:{attribute}" for attribute in attributes)
        params = {natural_col: row[natural_col]}
        params.update({a: row[a] for a in attributes})
        connection.execute(
            text(f"UPDATE {table} SET {assignments} WHERE {natural_col}=:{natural_col}"),
            params,
        )


def load_machine_scd2(connection, machines: pd.DataFrame, run_date: date) -> int:
    """Apply SCD Type 2 to machine attributes that require historical preservation."""
    versions_created = 0
    tracked = ["machine_name", "machine_type", "factory_id"]

    for row in machines.to_dict("records"):
        current = connection.execute(
            text(
                """
                SELECT machine_key, machine_name, machine_type, factory_id
                FROM dim_machine
                WHERE machine_id=:machine_id AND is_current=TRUE
                """
            ),
            {"machine_id": row["machine_id"]},
        ).mappings().first()

        if current and all(str(current[a]) == str(row[a]) for a in tracked):
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

        machine_key = next_key(connection, "dim_machine", "machine_key")
        connection.execute(
            text(
                """
                INSERT INTO dim_machine(
                    machine_key, machine_id, machine_name, machine_type,
                    factory_id, effective_date, expiry_date, is_current
                ) VALUES (
                    :machine_key, :machine_id, :machine_name, :machine_type,
                    :factory_id, :effective_date, :expiry_date, TRUE
                )
                """
            ),
            {
                "machine_key": machine_key,
                "machine_id": row["machine_id"],
                "machine_name": row["machine_name"],
                "machine_type": row["machine_type"],
                "factory_id": row["factory_id"],
                "effective_date": run_date,
                "expiry_date": date(9999, 12, 31),
            },
        )
        versions_created += 1

    return versions_created


def dimension_key(connection, table, key_col, natural_col, value) -> int:
    result = connection.execute(
        text(f"SELECT {key_col} FROM {table} WHERE {natural_col}=:value"),
        {"value": value},
    ).scalar_one_or_none()
    if result is None:
        raise ValueError(f"Dimension lookup failed: {table}.{natural_col}={value}")
    return int(result)


def machine_key_for_date(connection, machine_id: str, production_date: date) -> int:
    """Resolve the machine surrogate key that was valid on the production date."""
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
    """Incrementally load facts using Production_ID as the idempotency key."""
    inserted = 0

    for row in production.to_dict("records"):
        production_id = str(row["production_id"])
        duplicate = connection.execute(
            text("SELECT 1 FROM fact_production WHERE production_id=:production_id"),
            {"production_id": production_id},
        ).first()
        if duplicate:
            continue

        prod_date = pd.to_datetime(row["production_date"]).date()
        params = {
            "production_key": next_key(connection, "fact_production", "production_key"),
            "production_id": production_id,
            "date_key": int(prod_date.strftime("%Y%m%d")),
            "product_key": dimension_key(connection, "dim_product", "product_key", "product_id", row["product_id"]),
            "machine_key": machine_key_for_date(connection, row["machine_id"], prod_date),
            "factory_key": dimension_key(connection, "dim_factory", "factory_key", "factory_id", row["factory_id"]),
            "employee_key": dimension_key(connection, "dim_employee", "employee_key", "employee_id", row["employee_id"]),
            "shift_key": dimension_key(connection, "dim_shift", "shift_key", "shift_id", row["shift_id"]),
            "quantity_produced": int(row["quantity"]),
            "production_cost": float(row["production_cost"]),
            "production_time": int(row["production_time"]),
            "defect_count": int(row["defect_count"]),
        }

        connection.execute(
            text(
                """
                INSERT INTO fact_production(
                    production_key, production_id, date_key, product_key, machine_key,
                    factory_key, employee_key, shift_key, quantity_produced,
                    production_cost, production_time, defect_count
                ) VALUES (
                    :production_key, :production_id, :date_key, :product_key, :machine_key,
                    :factory_key, :employee_key, :shift_key, :quantity_produced,
                    :production_cost, :production_time, :defect_count
                )
                """
            ),
            params,
        )
        inserted += 1

    return inserted


def run(source_dir: Path, run_date: date, database_url: str) -> None:
    engine = create_engine(database_url)
    raw = extract(source_dir)
    data = {name: clean(df) for name, df in raw.items()}
    validate_sources(data)

    with engine.begin() as connection:
        ensure_run_log(connection)
        stage(data, connection)

        load_date_dimension(connection, data["production"])
        load_simple_dimension(connection, data["product"], "dim_product", "product_key", "product_id", ["product_name", "category", "unit_cost"])
        load_simple_dimension(connection, data["factory"], "dim_factory", "factory_key", "factory_id", ["factory_name", "location", "capacity"])
        load_simple_dimension(connection, data["employee"], "dim_employee", "employee_key", "employee_id", ["employee_name", "department", "role"])
        load_simple_dimension(connection, data["shift"], "dim_shift", "shift_key", "shift_id", ["shift_name", "start_time", "end_time"])

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

    print(
        "ETL SUCCESS | "
        f"run_date={run_date} | facts_inserted={facts_inserted} | "
        f"machine_versions_created={machine_versions}"
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Enterprise Manufacturing DW ETL")
    parser.add_argument("--source-dir", required=True)
    parser.add_argument("--run-date", required=True, help="YYYY-MM-DD")
    args = parser.parse_args()

    database_url = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/manufacturing_dw",
    )
    run(Path(args.source_dir), date.fromisoformat(args.run_date), database_url)


if __name__ == "__main__":
    main()
