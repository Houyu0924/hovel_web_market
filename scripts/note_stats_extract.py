#!/usr/bin/env python3
"""Extract note article metrics from the logged-in analytics page.

Runs locally with a persistent Chrome profile. No cookies or page dumps are
committed. The script writes only normalized metrics and a diagnostic JSON file.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = Path.home() / ".hovel-playwright-profile"
OUTPUT_DIR = ROOT / "data-collector" / "local-output" / "note"
CSV_PATH = OUTPUT_DIR / "note_article_metrics.csv"
DIAGNOSTIC_PATH = OUTPUT_DIR / "note_extract_diagnostic.json"
STATS_URL = "https://note.com/sitesettings/stats"

NUMBER_RE = re.compile(r"^\s*([0-9][0-9,]*)\s*$")


def to_int(value: str) -> int | None:
    match = NUMBER_RE.match(value)
    if not match:
        return None
    return int(match.group(1).replace(",", ""))


def normalize(text: str) -> str:
    return " ".join(text.replace("\u3000", " ").split())


def split_tokens(text: str) -> list[str]:
    """Split row text on line breaks and tabs without losing metric boundaries."""
    return [normalize(token) for token in re.split(r"[\n\t]+", text) if normalize(token)]


def extract_candidates(page) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return article rows and diagnostics using several DOM heuristics."""
    diagnostics: list[dict[str, Any]] = []
    rows: list[dict[str, Any]] = []

    selectors = [
        "table tbody tr",
        "[role='row']",
        "li",
        "article",
        "div",
    ]

    seen_titles: set[str] = set()

    for selector in selectors:
        locators = page.locator(selector)
        count = min(locators.count(), 2000)
        matched = 0

        for index in range(count):
            item = locators.nth(index)
            try:
                raw_text = item.inner_text(timeout=500)
            except Exception:
                continue

            if not raw_text or len(raw_text) > 700:
                continue

            tokens = split_tokens(raw_text)
            numbers = [to_int(token) for token in tokens]
            numbers = [number for number in numbers if number is not None]

            non_numbers = [token for token in tokens if to_int(token) is None]
            title_candidates = [
                token
                for token in non_numbers
                if 4 <= len(token) <= 140
                and token not in {"ビュー", "コメント", "スキ", "全期間", "週", "月", "年"}
                and not re.fullmatch(r"\d{4}[./-]\d{1,2}[./-]\d{1,2}.*", token)
            ]

            if len(numbers) < 3 or not title_candidates:
                continue

            title = max(title_candidates, key=len)
            if title in seen_titles:
                continue

            views, comments, likes = numbers[-3:]

            rows.append(
                {
                    "captured_at": datetime.now().isoformat(timespec="seconds"),
                    "title": title,
                    "views": views,
                    "comments": comments,
                    "likes": likes,
                    "source_selector": selector,
                }
            )
            seen_titles.add(title)
            matched += 1

        diagnostics.append(
            {"selector": selector, "elements_scanned": count, "rows_matched": matched}
        )

        if rows:
            break

    return rows, diagnostics


def write_csv(rows: list[dict[str, Any]]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fieldnames = ["captured_at", "title", "views", "comments", "likes"]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as playwright:
        context = playwright.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=False,
            viewport={"width": 1440, "height": 1000},
        )
        page = context.pages[0] if context.pages else context.new_page()
        page.goto(STATS_URL, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(5_000)

        if "login" in page.url:
            print("ERROR: note login session is unavailable.", file=sys.stderr)
            context.close()
            return 1

        rows, diagnostics = extract_candidates(page)
        payload = {
            "captured_at": datetime.now().isoformat(timespec="seconds"),
            "url": page.url,
            "title": page.title(),
            "article_rows_found": len(rows),
            "diagnostics": diagnostics,
            "sample_rows": rows[:5],
        }
        DIAGNOSTIC_PATH.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        if not rows:
            print(
                "ERROR: No article rows were extracted. "
                f"Review {DIAGNOSTIC_PATH} and rerun note_stats_probe.py.",
                file=sys.stderr,
            )
            context.close()
            return 2

        write_csv(rows)
        print(f"Extracted {len(rows)} article rows.")
        print(f"CSV: {CSV_PATH}")
        print(f"Diagnostic: {DIAGNOSTIC_PATH}")
        context.close()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
