#!/usr/bin/env python3
"""Validate transformed SL line data from a JSON file."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_FIELDS = ("line_id", "name", "transport_mode", "category")


def validate_transformed_records(records: list[dict[str, Any]]) -> None:
    """Raise ValueError when the transformed records do not match the expected schema."""
    if not isinstance(records, list):
        raise TypeError("Transformed data must be a list of records.")

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            raise TypeError(f"Record {index} must be an object, got {type(record).__name__}.")

        missing_fields = [field for field in REQUIRED_FIELDS if field not in record]
        if missing_fields:
            raise ValueError(
                f"Record {index} is missing required field(s): {', '.join(missing_fields)}."
            )

        line_id = record["line_id"]
        if line_id is None or line_id == "":
            raise ValueError(f"Record {index} has an empty line_id.")

        name = record["name"]
        if name is None:
            raise ValueError(f"Record {index} has a null name.")
        if not isinstance(name, str):
            raise ValueError(f"Record {index} has an invalid name.")

        transport_mode = record["transport_mode"]
        if not isinstance(transport_mode, str) or not transport_mode.strip():
            raise ValueError(f"Record {index} has an invalid transport_mode.")

        category = record["category"]
        if not isinstance(category, str) or not category.strip():
            raise ValueError(f"Record {index} has an invalid category.")


def load_json_records(input_path: str | Path) -> list[dict[str, Any]]:
    """Load transformed records from a JSON file, accepting either a list or a payload wrapper."""
    path = Path(input_path)
    with path.open("r", encoding="utf-8") as infile:
        payload = json.load(infile)

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]

    raise ValueError(f"JSON file '{path}' does not contain a list of transformed records.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate transformed SL line JSON data.")
    parser.add_argument("--input", default="data/sl_lines_transformed.json", help="Path to transformed JSON file")
    args = parser.parse_args()

    records = load_json_records(args.input)
    validate_transformed_records(records)

    print(f"Validated {len(records)} transformed records in {args.input}")


if __name__ == "__main__":
    main()
