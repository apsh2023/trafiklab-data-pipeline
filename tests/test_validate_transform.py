import pytest

from scripts.validate_transform import validate_transformed_records


def test_validate_transformed_records_accepts_clean_data():
    records = [
        {
            "line_id": 10,
            "name": "Blå linjen",
            "transport_mode": "METRO",
            "category": "metro",
        },
        {
            "line_id": 100,
            "name": "Bus 1",
            "transport_mode": "BUS",
            "category": "bus",
        },
    ]

    assert validate_transformed_records(records) is None


def test_validate_transformed_records_rejects_missing_or_invalid_fields():
    records = [{"line_id": 7, "name": "", "transport_mode": "TRAM"}]

    with pytest.raises(ValueError, match="category"):
        validate_transformed_records(records)
