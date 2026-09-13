#!/usr/bin/env python3
"""Aggregate transformed SL line records by category and transport mode."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from scripts.validate_transform import validate_transformed_records


def aggregate_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build a summary of total records, categories, and transport modes."""
    validate_transformed_records(records)

    category_counts: Counter[str] = Counter()
    transport_mode_counts: Counter[str] = Counter()

    for record in records:
        category = record["category"]
        transport_mode = record["transport_mode"]
        category_counts[category] += 1
        transport_mode_counts[transport_mode] += 1

    return {
        "total_records": len(records),
        "category_counts": dict(sorted(category_counts.items())),
        "transport_mode_counts": dict(sorted(transport_mode_counts.items())),
    }


def load_records(input_path: str | Path) -> list[dict[str, Any]]:
    """Load transformed records from a JSON file."""
    path = Path(input_path)
    with path.open("r", encoding="utf-8") as infile:
        payload = json.load(infile)

    if isinstance(payload, list):
        return payload

    if isinstance(payload, dict) and isinstance(payload.get("records"), list):
        return payload["records"]

    raise ValueError(f"JSON file '{path}' does not contain a list of transformed records.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate transformed SL line records into summary counts.")
    parser.add_argument("--input", default="data/sl_lines_transformed.json", help="Path to the transformed JSON file")
    parser.add_argument("--output", default="data/sl_lines_aggregated.json", help="Path to save aggregation output")
    args = parser.parse_args()

    records = load_records(args.input)
    summary = aggregate_records(records)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Aggregated {summary['total_records']} records and saved them to {output_path}")


if __name__ == "__main__":
    main()
