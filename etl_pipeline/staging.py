"""Staging layer loader."""


def load_to_staging(data, connection, table_name):
    """Load extracted data into staging tables."""
    data.to_sql(table_name, connection, if_exists="replace", index=False)


if __name__ == "__main__":
    print("Staging module ready")
