import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.fetch_sl_lines import build_summary, flatten_categories


def test_flatten_categories_creates_one_record_per_item():
    payload = {
        "metro": [
            {"id": 10, "name": "Blå linjen", "transport_mode": "METRO"},
            {"id": 11, "name": "Blå linjen 2", "transport_mode": "METRO"},
        ],
        "bus": [{"id": 100, "name": "Bus 1", "transport_mode": "BUS"}],
    }

    records = flatten_categories(payload)

    assert len(records) == 3
    assert records[0]["category"] == "metro"
    assert records[2]["category"] == "bus"
    assert records[2]["name"] == "Bus 1"


def test_build_summary_counts_categories_and_modes():
    records = [
        {"category": "metro", "transport_mode": "METRO"},
        {"category": "metro", "transport_mode": "METRO"},
        {"category": "bus", "transport_mode": "BUS"},
    ]

    summary = build_summary(records)

    assert summary["total_records"] == 3
    assert summary["category_counts"]["bus"] == 1
    assert summary["category_counts"]["metro"] == 2
    assert summary["transport_mode_counts"]["BUS"] == 1
    assert summary["transport_mode_counts"]["METRO"] == 2
