"""Transformation and data quality functions."""


def standardize_text(value):
    if value is None:
        return value
    return str(value).strip().title()


def remove_duplicates(df):
    return df.drop_duplicates()


if __name__ == "__main__":
    print("Transformation module ready")
