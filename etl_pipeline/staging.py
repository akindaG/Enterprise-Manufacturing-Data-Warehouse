"""Controlled staging-table loads for validated source snapshots."""

from __future__ import annotations

import pandas as pd
from sqlalchemy import text


def load_to_staging(data: dict[str, pd.DataFrame], connection) -> None:
    """Truncate predefined staging tables and bulk append the current snapshot."""
    for entity, frame in data.items():
        table = f"stg_{entity}"
        connection.execute(text(f"TRUNCATE TABLE {table}"))
        frame.to_sql(table, connection, if_exists="append", index=False, method="multi")
