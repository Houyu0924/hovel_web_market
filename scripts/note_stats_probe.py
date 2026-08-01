#!/usr/bin/env python3
"""Probe the logged-in note analytics page and export evidence for selector tuning.

Run locally on macOS with the same persistent Chrome profile used for note login.
This script does not store credentials in the repository.
"""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright

PROFILE_DIR = Path.home() / ".hovel-playwright-profile"
OUTPUT_DIR = Path("data-collector/local-output/note")
TARGET_URL = "https://note.com/sitesettings/stats"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR),
            channel="chrome",
            headless=False,
        )

        page = context.pages[0] if context.pages else context.new_page()
        page.goto(TARGET_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        metadata = {
            "url": page.url,
            "title": page.title(),
        }

        (OUTPUT_DIR / "page-metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        (OUTPUT_DIR / "page.html").write_text(page.content(), encoding="utf-8")
        page.screenshot(path=str(OUTPUT_DIR / "page.png"), full_page=True)

        body_text = page.locator("body").inner_text()
        (OUTPUT_DIR / "body.txt").write_text(body_text, encoding="utf-8")

        print("Saved:")
        print(f"- {OUTPUT_DIR / 'page-metadata.json'}")
        print(f"- {OUTPUT_DIR / 'page.html'}")
        print(f"- {OUTPUT_DIR / 'page.png'}")
        print(f"- {OUTPUT_DIR / 'body.txt'}")
        print("\nKeep this browser open and confirm the analytics page is visible.")
        input("Press Enter to close the browser: ")

        context.close()


if __name__ == "__main__":
    main()
