"""Extract layer for Manufacturing Data Warehouse ETL."""

import pandas as pd


def extract_csv(file_path):
    """Extract data from CSV source systems."""
    return pd.read_csv(file_path)


if __name__ == "__main__":
    print("Extraction module ready")
