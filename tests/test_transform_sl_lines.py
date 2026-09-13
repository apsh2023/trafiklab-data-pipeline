import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.transform_sl_lines import transform_lines


def test_transform_creates_one_record_per_line():
    payload = {
        "metro": [
            {"id": 10, "name": "Blå linjen", "transport_mode": "METRO"},
            {"id": 11, "name": "Blå linjen", "transport_mode": "METRO"},
        ],
        "bus": [{"id": 100, "name": "Bus 1", "transport_mode": "BUS"}],
    }

    records = transform_lines(payload)

    assert len(records) == 3
    assert records[0] == {
        "line_id": 10,
        "name": "Blå linjen",
        "transport_mode": "METRO",
        "category": "metro",
    }
    assert records[2] == {
        "line_id": 100,
        "name": "Bus 1",
        "transport_mode": "BUS",
        "category": "bus",
    }


def test_transform_keeps_only_required_fields():
    payload = {
        "tram": [
            {
                "id": 7,
                "name": "Nockebybanan",
                "transport_mode": "TRAM",
                "designation": "7",
                "group_of_lines": "Tram",
            }
        ]
    }

    records = transform_lines(payload)

    assert records == [
        {
            "line_id": 7,
            "name": "Nockebybanan",
            "transport_mode": "TRAM",
            "category": "tram",
        }
    ]
    assert set(records[0].keys()) == {"line_id", "name", "transport_mode", "category"}
