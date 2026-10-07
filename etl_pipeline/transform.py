"""Deterministic transformation helpers used before warehouse loading."""

from __future__ import annotations

import pandas as pd


def clean_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize headers/text and remove exact duplicate rows."""
    result = df.copy()
    result.columns = [column.strip().lower() for column in result.columns]
    result = result.drop_duplicates().reset_index(drop=True)
    for column in result.select_dtypes(include="object").columns:
        result[column] = result[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )
    return result


def clean_source_state(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    return {name: clean_frame(frame) for name, frame in data.items()}
