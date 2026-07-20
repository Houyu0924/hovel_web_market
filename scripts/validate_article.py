from pathlib import Path
import argparse
import sys

REQUIRED = [
    "title:", "slug:", "category:", "status:",
    "primary_keyword:", "search_intent:",
    "> 本記事にはアフィリエイトリンクが含まれます。",
    "## 選定基準", "## 比較表", "## まとめ",
]

parser = argparse.ArgumentParser()
parser.add_argument("path")
args = parser.parse_args()

path = Path(args.path)
if not path.exists():
    raise SystemExit(f"Not found: {path}")

text = path.read_text(encoding="utf-8")
missing = [item for item in REQUIRED if item not in text]
forbidden = ["実際に使ってみると", "絶対に改善", "必ず眠れる"]

if missing:
    print("Missing:")
    for item in missing:
        print(f"- {item}")

hits = [item for item in forbidden if item in text]
if hits:
    print("Risky expressions:")
    for item in hits:
        print(f"- {item}")

sys.exit(1 if missing or hits else 0)
