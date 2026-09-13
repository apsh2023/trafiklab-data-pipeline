#!/usr/bin/env python3
"""Generate an HTML report from aggregated SL line counts."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


def load_summary(input_path: str | Path) -> dict[str, Any]:
    """Load aggregate stats from a JSON file."""
    path = Path(input_path)
    with path.open("r", encoding="utf-8") as infile:
        payload = json.load(infile)

    if not isinstance(payload, dict):
        raise ValueError(f"Summary file '{path}' must contain a JSON object.")

    required_keys = {"total_records", "category_counts", "transport_mode_counts"}
    missing = sorted(required_keys - set(payload))
    if missing:
        raise ValueError(f"Summary file '{path}' is missing keys: {', '.join(missing)}")

    return payload


def render_table(title: str, rows: dict[str, int]) -> str:
    """Return a rendered HTML table for a section of stats."""
    table_rows = "".join(
        f"<tr><td>{html.escape(str(label))}</td><td>{value}</td></tr>"
        for label, value in rows.items()
    )

    return f"""
    <section class=\"card\">
      <h2>{html.escape(title)}</h2>
      <table>
        <thead>
          <tr><th>Label</th><th>Count</th></tr>
        </thead>
        <tbody>
          {table_rows}
        </tbody>
      </table>
    </section>
    """


def build_report_html(summary: dict[str, Any]) -> str:
    """Create a simple HTML report for aggregated SL line data."""
    total_records = summary.get("total_records", 0)
    category_counts = summary.get("category_counts", {})
    transport_mode_counts = summary.get("transport_mode_counts", {})

    return f"""<!DOCTYPE html>
<html lang=\"en\">
  <head>
    <meta charset=\"UTF-8\" />
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
    <title>SL Line Aggregation Report</title>
    <style>
      :root {{
        color-scheme: light;
        --bg: #f4f7fb;
        --card: #ffffff;
        --text: #1f2937;
        --muted: #6b7280;
        --border: #dbe3ee;
        --accent: #2563eb;
      }}
      body {{
        font-family: Arial, sans-serif;
        background: var(--bg);
        color: var(--text);
        margin: 0;
        padding: 2rem;
      }}
      h1, h2 {{
        margin-top: 0;
      }}
      .container {{
        max-width: 980px;
        margin: 0 auto;
      }}
      .summary {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
      }}
      .summary .total {{
        font-size: 2.2rem;
        font-weight: 700;
        color: var(--accent);
      }}
      .grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin-top: 1.5rem;
      }}
      .card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.25rem;
      }}
      table {{
        width: 100%;
        border-collapse: collapse;
      }}
      th, td {{
        text-align: left;
        padding: 0.7rem 0.75rem;
        border-bottom: 1px solid var(--border);
      }}
      th {{
        background: #eef4ff;
      }}
      .muted {{
        color: var(--muted);
      }}
    </style>
  </head>
  <body>
    <div class=\"container\">
      <div class=\"summary\">
        <p class=\"muted\">SL Line Aggregation Report</p>
        <h1>Total records</h1>
        <div class=\"total\">{total_records}</div>
      </div>

      <div class=\"grid\">
        {render_table('Category counts', category_counts)}
        {render_table('Transport mode counts', transport_mode_counts)}
      </div>
    </div>
  </body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Create an HTML report from aggregated SL line data.")
    parser.add_argument("--input", default="data/sl_lines_summary.json", help="Path to the aggregated summary JSON file")
    parser.add_argument("--output", default="reports/aggregate_report.html", help="Path to the generated HTML report")
    args = parser.parse_args()

    summary = load_summary(args.input)
    report_html = build_report_html(summary)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report_html, encoding="utf-8")

    print(f"Generated HTML report at {output_path}")


if __name__ == "__main__":
    main()
