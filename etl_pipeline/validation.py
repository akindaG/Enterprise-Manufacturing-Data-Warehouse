"""ETL validation checks."""


def validate_not_empty(df):
    return len(df) > 0


def validate_no_null_keys(df, columns):
    return df[columns].isnull().sum().sum() == 0


if __name__ == "__main__":
    print("Validation module ready")
