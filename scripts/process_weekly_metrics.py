#!/usr/bin/env python3
"""Process HOVEL weekly input into normalized CSV files.

This script uses only the Python standard library.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data-collector" / "inbox" / "weekly-input.csv"

OUTPUTS = {
    "note": ROOT / "data" / "note" / "weekly_metrics.csv",
    "x": ROOT / "data" / "x" / "account_metrics.csv",
    "amazon": ROOT / "data" / "amazon" / "associate_metrics.csv",
    "gsc": ROOT / "data" / "search-console" / "weekly_metrics.csv",
}

REQUIRED = [
    "week",
    "start_date",
    "end_date",
    "note_pv",
    "note_likes",
    "note_comments",
    "note_articles_published",
    "x_followers",
    "amazon_clicks",
    "amazon_orders",
    "amazon_revenue_jpy",
]

NUMERIC = [
    "note_pv",
    "note_likes",
    "note_comments",
    "note_articles_published",
    "x_followers",
    "x_impressions",
    "x_likes",
    "x_reposts",
    "x_replies",
    "x_profile_visits",
    "x_url_clicks",
    "amazon_clicks",
    "amazon_orders",
    "amazon_revenue_jpy",
    "gsc_clicks",
    "gsc_impressions",
    "gsc_ctr_percent",
    "gsc_average_position",
]


def load_latest() -> dict[str, str]:
    if not INPUT.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT}")
    with INPUT.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("weekly-input.csv has no data rows")
    return rows[-1]


def validate(row: dict[str, str]) -> None:
    missing = [key for key in REQUIRED if not (row.get(key) or "").strip()]
    if missing:
        raise ValueError("Missing required fields: " + ", ".join(missing))
    for key in NUMERIC:
        value = (row.get(key) or "").strip()
        if not value:
            continue
        try:
            number = float(value)
        except ValueError as exc:
            raise ValueError(f"{key} must be numeric: {value}") from exc
        if number < 0:
            raise ValueError(f"{key} must be zero or greater")


def append_unique(path: Path, fieldnames: list[str], record: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, str]] = []
    if path.exists():
        with path.open(encoding="utf-8-sig", newline="") as f:
            existing = list(csv.DictReader(f))
        if any(item.get("week") == record["week"] for item in existing):
            raise ValueError(f"Week {record['week']} already exists in {path}")
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not existing:
            writer.writeheader()
        writer.writerow(record)


def main() -> int:
    try:
        row = load_latest()
        validate(row)

        common = {
            "week": row["week"],
            "start_date": row["start_date"],
            "end_date": row["end_date"],
        }

        note = common | {
            "pv": row["note_pv"],
            "likes": row["note_likes"],
            "comments": row["note_comments"],
            "articles_published": row["note_articles_published"],
        }
        x = common | {
            "followers": row["x_followers"],
            "impressions": row.get("x_impressions", ""),
            "likes": row.get("x_likes", ""),
            "reposts": row.get("x_reposts", ""),
            "replies": row.get("x_replies", ""),
            "profile_visits": row.get("x_profile_visits", ""),
            "url_clicks": row.get("x_url_clicks", ""),
        }
        amazon = common | {
            "clicks": row["amazon_clicks"],
            "orders": row["amazon_orders"],
            "revenue_jpy": row["amazon_revenue_jpy"],
        }
        gsc = common | {
            "clicks": row.get("gsc_clicks", ""),
            "impressions": row.get("gsc_impressions", ""),
            "ctr_percent": row.get("gsc_ctr_percent", ""),
            "average_position": row.get("gsc_average_position", ""),
        }

        append_unique(OUTPUTS["note"], list(note), note)
        append_unique(OUTPUTS["x"], list(x), x)
        append_unique(OUTPUTS["amazon"], list(amazon), amazon)
        append_unique(OUTPUTS["gsc"], list(gsc), gsc)

        print(f"Processed {row['week']} successfully.")
        return 0
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
