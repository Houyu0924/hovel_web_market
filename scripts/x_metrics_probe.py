#!/usr/bin/env python3
"""Probe X analytics/post pages with a local persistent Chrome profile.

This script is intentionally diagnostic. It does not attempt to bypass login,
anti-bot controls, or platform restrictions. It opens a user-supplied X URL,
waits for manual confirmation if needed, and saves local-only artifacts for
selector development.

Usage:
    python3 scripts/x_metrics_probe.py
    X_METRICS_URL="https://x.com/i/account_analytics" python3 scripts/x_metrics_probe.py

Outputs are written under data-collector/local-output/x/ and must not be
committed because they may contain account-specific information.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PROFILE_DIR = Path.home() / ".hovel-playwright-profile-x"
OUTPUT_DIR = ROOT / "data-collector" / "local-output" / "x"
TARGET_URL = os.environ.get("X_METRICS_URL", "https://x.com/home")


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
        page.goto(TARGET_URL, wait_until="domcontentloaded", timeout=60_000)
        page.wait_for_timeout(5_000)

        print("Xの対象画面を表示してください。ログインが必要なら手動で行ってください。")
        print("表示後、ターミナルに戻ってEnterを押してください。")
        input()

        captured_at = datetime.now().isoformat(timespec="seconds")
        metadata = {
            "captured_at": captured_at,
            "url": page.url,
            "title": page.title(),
        }

        (OUTPUT_DIR / "page-metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (OUTPUT_DIR / "body.txt").write_text(
            page.locator("body").inner_text(timeout=10_000), encoding="utf-8"
        )
        (OUTPUT_DIR / "page.html").write_text(page.content(), encoding="utf-8")
        page.screenshot(path=str(OUTPUT_DIR / "page.png"), full_page=True)

        # Capture a compact list of likely tweet/article containers for selector work.
        article_samples: list[dict[str, str]] = []
        articles = page.locator("article")
        for index in range(min(articles.count(), 100)):
            try:
                text = articles.nth(index).inner_text(timeout=1_000).strip()
            except Exception:
                continue
            if text:
                article_samples.append({"index": str(index), "text": text[:2000]})

        (OUTPUT_DIR / "article-samples.json").write_text(
            json.dumps(article_samples, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        print(f"Saved X probe output to: {OUTPUT_DIR}")
        print("Do not commit these local artifacts.")
        context.close()
        return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Cancelled.", file=sys.stderr)
        raise SystemExit(130)
