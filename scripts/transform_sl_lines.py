#!/usr/bin/env python3
"""Transform raw SL line payloads into a flat list of clean records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def transform_lines(raw_payload: dict) -> list[dict]:
    """Flatten the raw category-based SL API response into one clean record per line."""
    transformed: list[dict] = []

    for category, lines in raw_payload.items():
        if not isinstance(lines, list):
            continue

        for item in lines:
            if not isinstance(item, dict):
                continue

            transformed.append(
                {
                    "line_id": item.get("id"),
                    "name": item.get("name"),
                    "transport_mode": item.get("transport_mode"),
                    "category": category,
                }
            )

    return transformed


def main() -> None:
    parser = argparse.ArgumentParser(description="Transform raw SL line data into a flat list of clean records.")
    parser.add_argument("--input", default="data/sl_lines_raw.json", help="Path to the raw SL JSON payload")
    parser.add_argument("--output", default="data/sl_lines_transformed.json", help="Path to save the transformed JSON")
    args = parser.parse_args()

    input_path = Path(args.input)
    with input_path.open("r", encoding="utf-8") as infile:
        raw_payload = json.load(infile)

    transformed = transform_lines(raw_payload)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(transformed, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Transformed {len(transformed)} lines and saved them to {output_path}")


if __name__ == "__main__":
    main()
