#!/usr/bin/env python3
"""Fetch and summarize SL transport line data from the Trafiklab API."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_URL = "https://transport.integration.sl.se/v1/lines?transport_authority_id=1"


def fetch_json(url: str) -> dict:
    """Fetch a JSON payload from the given URL."""
    request = Request(
        url,
        headers={
            "Accept": "application/json",
            "User-Agent": "trafiklab-data-pipeline/1.0",
        },
    )

    try:
        with urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"HTTP error while fetching {url}: {exc}") from exc
    except URLError as exc:
        raise RuntimeError(f"Network error while fetching {url}: {exc}") from exc


def flatten_categories(payload: dict) -> list[dict]:
    """Convert the top-level category buckets into one flat list of records."""
    records: list[dict] = []

    for category_name, items in payload.items():
        if not isinstance(items, list):
            continue

        for item in items:
            if isinstance(item, dict):
                normalized = dict(item)
                normalized["category"] = category_name
                records.append(normalized)

    return records


def clean_record(record: dict) -> dict:
    """Normalize a single SL line record for downstream analysis."""
    return {
        "category": record.get("category", "unknown"),
        "id": record.get("id"),
        "name": record.get("name"),
        "designation": record.get("designation"),
        "transport_mode": record.get("transport_mode", "unknown"),
        "group_of_lines": record.get("group_of_lines", ""),
        "transport_authority": record.get("transport_authority", {}).get("name", ""),
        "contractor": record.get("contractor", {}).get("name", ""),
    }


def build_summary(records: list[dict]) -> dict:
    """Build a simple summary for the response data."""
    category_counter = Counter()
    transport_mode_counter = Counter()

    for record in records:
        category_counter[record.get("category", "unknown")] += 1
        transport_mode_counter[record.get("transport_mode", "unknown")] += 1

    return {
        "total_records": len(records),
        "category_counts": dict(sorted(category_counter.items())),
        "transport_mode_counts": dict(sorted(transport_mode_counter.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch SL line data from the API and generate a summary.")
    parser.add_argument("--url", default=API_URL, help="SL API endpoint to fetch")
    parser.add_argument("--output", default="data/sl_lines_raw.json", help="Path to save the raw JSON response")
    parser.add_argument(
        "--summary-output",
        default="data/sl_lines_summary.json",
        help="Path to save the normalized summary JSON",
    )
    args = parser.parse_args()

    raw_payload = fetch_json(args.url)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(raw_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    flattened_records = flatten_categories(raw_payload)
    cleaned_records = [clean_record(record) for record in flattened_records]

    summary = build_summary(cleaned_records)
    summary_path = Path(args.summary_output)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print("SL API fetch successful")
    print(f"Saved raw JSON to: {output_path}")
    print(f"Saved summary JSON to: {summary_path}")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
