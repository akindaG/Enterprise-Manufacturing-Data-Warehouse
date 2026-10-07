from datetime import date

from etl_pipeline.scd_type2 import create_new_version, expire_version, has_tracked_change


def test_scd_detects_factory_transfer():
    old = {"machine_name": "CNC-1", "machine_type": "CNC", "factory_id": "F001", "status": "Active"}
    new = {**old, "factory_id": "F002"}
    assert has_tracked_change(old, new)


def test_scd_ignores_unchanged_machine():
    record = {"machine_name": "CNC-1", "machine_type": "CNC", "factory_id": "F001", "status": "Active"}
    assert not has_tracked_change(record, record.copy())


def test_expiry_is_day_before_new_version():
    expired = expire_version({"machine_id": "M001"}, date(2026, 8, 15))
    assert expired["expiry_date"] == date(2026, 8, 14)
    assert expired["is_current"] is False


def test_new_version_is_current():
    current = create_new_version({"machine_id": "M001"}, date(2026, 8, 15))
    assert current["effective_date"] == date(2026, 8, 15)
    assert current["expiry_date"] == date(9999, 12, 31)
    assert current["is_current"] is True
