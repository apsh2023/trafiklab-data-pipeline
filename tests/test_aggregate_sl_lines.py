import pytest

from scripts.aggregate_sl_lines import aggregate_records


def test_aggregate_records_counts_categories_and_modes():
    records = [
        {"line_id": 10, "name": "Blå linjen", "transport_mode": "METRO", "category": "metro"},
        {"line_id": 20, "name": "Bus 1", "transport_mode": "BUS", "category": "bus"},
        {"line_id": 30, "name": "Blå linjen 2", "transport_mode": "METRO", "category": "metro"},
    ]

    summary = aggregate_records(records)

    assert summary["total_records"] == 3
    assert summary["category_counts"]["bus"] == 1
    assert summary["category_counts"]["metro"] == 2
    assert summary["transport_mode_counts"]["BUS"] == 1
    assert summary["transport_mode_counts"]["METRO"] == 2


def test_aggregate_records_rejects_missing_schema_fields():
    records = [{"line_id": 7, "name": "Tram", "transport_mode": "TRAM"}]

    with pytest.raises(ValueError, match="category"):
        aggregate_records(records)
