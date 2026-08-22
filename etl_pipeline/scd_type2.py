"""Reusable Slowly Changing Dimension Type 2 helper functions.

The executable database implementation lives in run_etl.py. These pure helpers are
kept separately so the SCD comparison and version semantics can be tested or reused.
"""

from __future__ import annotations

from datetime import date, timedelta

TRACKED_MACHINE_FIELDS = ("machine_name", "machine_type", "factory_id", "status")


def has_tracked_change(old_record: dict, new_record: dict) -> bool:
    """Return True when any tracked machine attribute has changed."""
    return any(
        str(old_record.get(field)) != str(new_record.get(field))
        for field in TRACKED_MACHINE_FIELDS
    )


def expire_version(record: dict, new_effective_date: date) -> dict:
    """Return an expired copy of an existing SCD Type 2 record."""
    return {
        **record,
        "expiry_date": new_effective_date - timedelta(days=1),
        "is_current": False,
    }


def create_new_version(record: dict, effective_date: date) -> dict:
    """Return a current SCD Type 2 version using project date semantics."""
    return {
        **record,
        "effective_date": effective_date,
        "expiry_date": date(9999, 12, 31),
        "is_current": True,
    }
