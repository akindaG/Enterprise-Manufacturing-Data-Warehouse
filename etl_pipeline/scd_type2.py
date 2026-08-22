"""Slowly Changing Dimension Type 2 implementation."""

from datetime import datetime


def detect_change(old_record, new_record):
    return old_record != new_record


def create_new_version(record):
    return {
        **record,
        "effective_date": datetime.now(),
        "current_flag": True
    }


if __name__ == "__main__":
    print("SCD Type 2 module ready")
