#!/usr/bin/env python3
"""Collect note dashboard metrics with a local Playwright browser session.

This script is intentionally local-only. It does not store cookies or credentials
in GitHub. On first run, use --login, sign in manually, then close the browser.
Later runs reuse the local browser profile directory.

Selectors are isolated in SELECTORS because note UI changes may require updates.
"""

from __future__ import annotations

import argparse
import csv
from datetime import date, timedelta
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / ".local" / "note-browser-profile"
OUT = ROOT / "data" / "note" / "weekly_metrics.csv"
DASHBOARD_URL = "https://note.com/sitesettings/stats"

SELECTORS = {
    "pv": "[data-testid='total-view-count']",
    "likes": "[data-testid='total-like-count']",
    "comments": "[data-testid='total-comment-count']",
}


def iso_week_range(year: int, week: int) -> tuple[date, date]:
    start = date.fromisocalendar(year, week, 1)
    return start, start + timedelta(days=6)


def parse_number(text: str) -> int:
    cleaned = text.replace(",", "").strip()
    digits = "".join(ch for ch in cleaned if ch.isdigit())
    if not digits:
        raise ValueError(f"Could not parse number from: {text!r}")
    return int(digits)


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
    parser.add_argument("--login", action="store_true", help="Open browser for manual login")
    args = parser.parse_args()

    year_text, week_text = args.week.split("-W", 1)
    start, end = iso_week_range(int(year_text), int(week_text))
    PROFILE.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE), headless=not args.login
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(DASHBOARD_URL, wait_until="domcontentloaded")

        if args.login:
            print("Log in to note in the opened browser, then press Enter here.")
            input()
            context.close()
            return 0

        values: dict[str, int] = {}
        for key, selector in SELECTORS.items():
            locator = page.locator(selector).first
            if locator.count() == 0:
                raise RuntimeError(
                    f"note selector not found for {key}: {selector}. "
                    "Update SELECTORS after checking the dashboard DOM."
                )
            values[key] = parse_number(locator.inner_text())
        context.close()

    record = {
        "week": args.week,
        "start_date": start.isoformat(),
        "end_date": end.isoformat(),
        "pv": str(values["pv"]),
        "likes": str(values["likes"]),
        "comments": str(values["comments"]),
        "articles_published": "",
    }
    append_unique(record)
    print(f"Collected note metrics for {args.week}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
