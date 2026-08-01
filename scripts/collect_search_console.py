#!/usr/bin/env python3
"""Collect weekly Google Search Console metrics.

Required environment variables:
- GSC_SITE_URL: property URL, e.g. https://example.com/
- GOOGLE_APPLICATION_CREDENTIALS: path to a service-account JSON file

The service account must be added as a user of the Search Console property.
"""

from __future__ import annotations

import argparse
import csv
import os
from datetime import date, timedelta
from pathlib import Path

from google.oauth2 import service_account
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "search-console" / "weekly_metrics.csv"
SCOPES = ["https://www.googleapis.com/auth/webmasters.readonly"]


def iso_week_range(year: int, week: int) -> tuple[date, date]:
    start = date.fromisocalendar(year, week, 1)
    return start, start + timedelta(days=6)


def append_unique(record: dict[str, str]) -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict[str, str]] = []
    if OUT.exists():
        with OUT.open(encoding="utf-8-sig", newline="") as f:
            existing = list(csv.DictReader(f))
        if any(row.get("week") == record["week"] for row in existing):
            raise ValueError(f"Week {record['week']} already exists in {OUT}")

    with OUT.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(record))
        if not existing:
            writer.writeheader()
        writer.writerow(record)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--week", required=True, help="ISO week, e.g. 2026-W31")
    args = parser.parse_args()

    site_url = os.environ.get("GSC_SITE_URL", "").strip()
    credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "").strip()
    if not site_url or not credentials_path:
        raise SystemExit("GSC_SITE_URL and GOOGLE_APPLICATION_CREDENTIALS are required")

    year_text, week_text = args.week.split("-W", 1)
    start, end = iso_week_range(int(year_text), int(week_text))

    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=SCOPES
    )
    service = build("searchconsole", "v1", credentials=credentials, cache_discovery=False)
    body = {
        "startDate": start.isoformat(),
        "endDate": end.isoformat(),
        "dimensions": [],
        "dataState": "final",
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    row = (response.get("rows") or [{}])[0]

    record = {
        "week": args.week,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "clicks": str(row.get("clicks", 0)),
        "impressions": str(row.get("impressions", 0)),
        "ctr_percent": str(round(float(row.get("ctr", 0)) * 100, 4)),
        "average_position": str(round(float(row.get("position", 0)), 4)),
    }
    append_unique(record)
    print(f"Collected Search Console metrics for {args.week}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
