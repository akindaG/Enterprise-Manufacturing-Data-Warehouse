"""Database helpers and ETL audit logging."""

from __future__ import annotations

from sqlalchemy import text


def ensure_run_log(connection) -> None:
    connection.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS etl_run_log (
                run_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
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
