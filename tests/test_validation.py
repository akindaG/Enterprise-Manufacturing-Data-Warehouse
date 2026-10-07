from datetime import date

import pandas as pd
import pytest

from etl_pipeline.validation import validate_sources


def valid_source_state():
    return {
        "product": pd.DataFrame([{"product_id": "P001", "product_name": "Widget", "category": "A", "unit_cost": 10.0}]),
        "factory": pd.DataFrame([{"factory_id": "F001", "factory_name": "Plant A", "location": "Colombo", "capacity": 1000}]),
        "machine": pd.DataFrame([{"machine_id": "M001", "machine_name": "CNC-1", "machine_type": "CNC", "factory_id": "F001", "status": "Active"}]),
        "employee": pd.DataFrame([{"employee_id": "E001", "employee_name": "Alex", "department": "Production", "role": "Operator"}]),
        "shift": pd.DataFrame([{"shift_id": "S001", "shift_name": "Day", "start_time": "08:00", "end_time": "16:00"}]),
        "production": pd.DataFrame([{
            "production_id": "PR001", "product_id": "P001", "machine_id": "M001",
            "factory_id": "F001", "employee_id": "E001", "shift_id": "S001",
            "production_date": "2026-08-01", "quantity": 100, "production_time": 60,
            "production_cost": 5000.0, "defect_count": 2,
        }]),
    }


def test_valid_source_state_passes():
    validate_sources(valid_source_state(), date(2026, 8, 1))


def test_defects_cannot_exceed_quantity():
    data = valid_source_state()
    data["production"].loc[0, "defect_count"] = 101
    with pytest.raises(ValueError, match="defect_count cannot exceed quantity"):
        validate_sources(data, date(2026, 8, 1))


def test_machine_factory_consistency_is_enforced():
    data = valid_source_state()
    data["factory"] = pd.concat([
        data["factory"],
        pd.DataFrame([{"factory_id": "F002", "factory_name": "Plant B", "location": "Kandy", "capacity": 800}]),
    ], ignore_index=True)
    data["production"].loc[0, "factory_id"] = "F002"
    with pytest.raises(ValueError, match="does not match the machine assignment"):
        validate_sources(data, date(2026, 8, 1))
