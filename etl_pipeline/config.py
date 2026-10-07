"""Configuration and source contracts for the manufacturing data platform."""

from __future__ import annotations

import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

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
    """Return a SQLAlchemy PostgreSQL URL without hardcoding credentials."""
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
