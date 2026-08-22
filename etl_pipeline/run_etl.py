"""End-to-end ETL orchestrator for the Enterprise Manufacturing Data Warehouse.

Run 1:
    python etl_pipeline/run_etl.py --source-dir source_data/run_1 --run-date 2026-08-01
Run 2:
    python etl_pipeline/run_etl.py --source-dir source_data/run_2 --run-date 2026-08-15

Configuration is read from environment variables or a local .env file. Copy
.env.example to .env for local development. DATABASE_URL, when supplied, takes
precedence over the individual DB_* settings.
"""

from __future__ import annotations

import argparse
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
from dotenv import load_dotenv
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
        "production_id", "product_id", "machine_id", "factory_id",
        "employee_id", "shift_id", "production_date", "quantity",
        "production_time", "production_cost", "defect_count",
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


def database_url_from_environment() -> str:
    """Build the SQLAlchemy PostgreSQL URL from environment configuration."""
    load_dotenv()
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    host = os.getenv("DB_HOST", "localhost")
    port = os.getenv("DB_PORT", "5432")
    name = os.getenv("DB_NAME", "manufacturing_dw")
    user = quote_plus(os.getenv("DB_USER", "postgres"))
    password = quote_plus(os.getenv("DB_PASSWORD", "postgres"))
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"


def extract(source_dir: Path) -> dict[str, pd.DataFrame]:
    """Read every required CSV extract from one reproducible source state."""
    data: dict[str, pd.DataFrame] = {}
    for name, filename in FILES.items():
        path = source_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing source file: {path}")
        data[name] = pd.read_csv(path)
    return data


def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize column names, trim text values and remove exact duplicate rows."""
    result = df.copy()
    result.columns = [column.strip().lower() for column in result.columns]
    result = result.drop_duplicates()
    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
    return result


def validate_sources(data: dict[str, pd.DataFrame], run_date: date) -> None:
    """Fail fast when a source state violates schema or business-quality rules."""
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

    # Referential-integrity checks before warehouse loading.
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


def stage(data: dict[str, pd.DataFrame], connection) -> None:
    """Load cleaned source extracts into reproducible staging tables."""
    for name, df in data.items():
        df.to_sql(f"stg_{name}", connection, if_exists="replace", index=False)


def next_key(connection, table: str, key_col: str) -> int:
    """Generate the next integer surrogate key in a warehouse table."""
    return int(
        connection.execute(
            text(f"SELECT COALESCE(MAX({key_col}), 0) + 1 FROM {table}")
        ).scalar_one()
    )


def ensure_run_log(connection) -> None:
    """Create an auditable ETL run log."""
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
    for production_date in dates:
        key = int(production_date.strftime("%Y%m%d"))
        if connection.execute(text("SELECT 1 FROM dim_date WHERE date_key=:key"), {"key": key}).first():
            continue
        connection.execute(
            text(
                """
                INSERT INTO dim_date(date_key, full_date, day, month, quarter, year)
                VALUES (:key, :full_date, :day, :month, :quarter, :year)
                """
            ),
            {
                "key": key,
                "full_date": production_date,
                "day": production_date.day,
                "month": production_date.month,
                "quarter": ((production_date.month - 1) // 3) + 1,
                "year": production_date.year,
            },
        )


def load_type1_dimension(connection, df, table, key_col, natural_col, attributes) -> None:
    """Insert new members and overwrite current values for Type 1 dimensions."""
    for row in df.to_dict("records"):
        existing = connection.execute(
            text(f"SELECT {key_col} FROM {table} WHERE {natural_col}=:natural_key"),
            {"natural_key": row[natural_col]},
        ).scalar_one_or_none()

        if existing is None:
            key = next_key(connection, table, key_col)
            columns = [key_col, natural_col] + attributes
            params = {key_col: key, natural_col: row[natural_col]}
            params.update({attribute: row[attribute] for attribute in attributes})
            connection.execute(
                text(
                    f"INSERT INTO {table} ({', '.join(columns)}) "
                    f"VALUES ({', '.join(':' + column for column in columns)})"
                ),
                params,
            )
            continue

        assignments = ", ".join(f"{attribute}=:{attribute}" for attribute in attributes)
        params = {natural_col: row[natural_col]}
        params.update({attribute: row[attribute] for attribute in attributes})
        connection.execute(
            text(f"UPDATE {table} SET {assignments} WHERE {natural_col}=:{natural_col}"),
            params,
        )


def load_machine_scd2(connection, machines: pd.DataFrame, run_date: date) -> int:
    """Apply SCD Type 2 to machine attributes requiring historical preservation."""
    versions_created = 0
    tracked_source_columns = ["machine_name", "machine_type", "factory_id", "status"]

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

        current_values = None
        if current:
            current_values = {
                "machine_name": current["machine_name"],
                "machine_type": current["machine_type"],
                "factory_id": current["factory_id"],
                "status": current["machine_status"],
            }

        if current_values and all(
            str(current_values[column]) == str(row[column])
            for column in tracked_source_columns
        ):
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
                    factory_id, machine_status, effective_date, expiry_date, is_current
                ) VALUES (
                    :machine_key, :machine_id, :machine_name, :machine_type,
                    :factory_id, :machine_status, :effective_date, :expiry_date, TRUE
                )
                """
            ),
            {
                "machine_key": machine_key,
                "machine_id": row["machine_id"],
                "machine_name": row["machine_name"],
                "machine_type": row["machine_type"],
                "factory_id": row["factory_id"],
                "machine_status": row["status"],
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
    """Resolve the machine surrogate key valid on the production event date."""
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
        if connection.execute(
            text("SELECT 1 FROM fact_production WHERE production_id=:production_id"),
            {"production_id": production_id},
        ).first():
            continue

        production_date = pd.to_datetime(row["production_date"]).date()
        params = {
            "production_key": next_key(connection, "fact_production", "production_key"),
            "production_id": production_id,
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
    validate_sources(data, run_date)

    with engine.begin() as connection:
        ensure_run_log(connection)
        stage(data, connection)

        load_date_dimension(connection, data["production"])
        load_type1_dimension(connection, data["product"], "dim_product", "product_key", "product_id", ["product_name", "category", "unit_cost"])
        load_type1_dimension(connection, data["factory"], "dim_factory", "factory_key", "factory_id", ["factory_name", "location", "capacity"])
        load_type1_dimension(connection, data["employee"], "dim_employee", "employee_key", "employee_id", ["employee_name", "department", "role"])
        load_type1_dimension(connection, data["shift"], "dim_shift", "shift_key", "shift_id", ["shift_name", "start_time", "end_time"])

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
    run(Path(args.source_dir), date.fromisoformat(args.run_date), database_url_from_environment())


if __name__ == "__main__":
    main()
