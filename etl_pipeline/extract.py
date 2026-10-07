"""Source extraction for reproducible manufacturing snapshots."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from etl_pipeline.config import FILES


def extract_source_state(source_dir: Path) -> dict[str, pd.DataFrame]:
    """Read every required CSV from one source-state directory."""
    data: dict[str, pd.DataFrame] = {}
    for entity, filename in FILES.items():
        path = source_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing source file: {path}")
        data[entity] = pd.read_csv(path)
    return data
