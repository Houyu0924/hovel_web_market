#!/usr/bin/env python3
"""Dependency-free quality gate for HOVEL Markdown articles."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REQUIRED_FRONTMATTER = ("title:", "status:", "reviewed:")
RISK_PATTERNS = {
    "guarantee": re.compile(r"必ず|絶対に|確実に|100%"),
    "medical_claim": re.compile(r"治る|完治|治療できる|診断できる"),
    "fake_experience": re.compile(r"使ってみた|実際に使用した|愛用している"),
    "placeholder": re.compile(r"TODO|TBD|要確認|仮リンク|example\.com", re.IGNORECASE),
}


def inspect(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if not text.startswith("---\n"):
        errors.append("front matter がありません")
    else:
        end = text.find("\n---\n", 4)
        front = text[: end + 5] if end >= 0 else ""
        if not front:
            errors.append("front matter が閉じられていません")
        else:
            for field in REQUIRED_FRONTMATTER:
                if field not in front:
                    errors.append(f"front matter の必須項目不足: {field}")

    if len(text.strip()) < 800:
        errors.append("本文が800文字未満です")
    if "# " not in text:
        errors.append("H1見出しがありません")
    if text.count("## ") < 2:
        errors.append("H2見出しが2個未満です")

    for name, pattern in RISK_PATTERNS.items():
        matches = sorted(set(pattern.findall(text)))
        if matches:
            errors.append(f"要手動確認[{name}]: {', '.join(matches[:5])}")

    affiliate_markers = ("amazon", "アソシエイト", "affiliate", "楽天市場")
    if any(marker.lower() in text.lower() for marker in affiliate_markers):
        if "広告" not in text and "アフィリエイト" not in text:
            errors.append("広告・アフィリエイト表記が見つかりません")

    if re.search(r"https?://", text) and "参考" not in text and "出典" not in text:
        errors.append("URLがありますが参考文献または出典セクションがありません")

    return errors


def markdown_files(root: Path) -> list[Path]:
    candidates = list((root / "content" / "drafts").glob("*.md"))
    candidates += list((root / "content" / "published").glob("*.md"))
    return sorted(set(candidates))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="*")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    files = [Path(p).resolve() for p in args.paths] or markdown_files(root)
    if not files:
        print("No Markdown articles found; quality gate skipped.")
        return 0

    failed = False
    for path in files:
        errors = inspect(path)
        if errors:
            failed = True
            print(f"FAIL: {path}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS: {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
