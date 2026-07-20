from pathlib import Path
from datetime import date
import argparse
import re

def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", "-", text)
    text = re.sub(r"[^\w\-ぁ-んァ-ヶ一-龠々ー]", "", text)
    return text[:80] or "article"

parser = argparse.ArgumentParser()
parser.add_argument("--keyword", required=True)
parser.add_argument("--type", default="comparison")
parser.add_argument("--priority", default="B")
args = parser.parse_args()

root = Path(__file__).resolve().parents[1]
template = (root / "templates" / "job.md").read_text(encoding="utf-8")
today = date.today().isoformat()
slug = slugify(args.keyword)
job_id = f"{today}-{slug}"
content = template.replace("job_id:", f"job_id: {job_id}", 1)
content = content.replace("keyword:", f"keyword: {args.keyword}", 1)
content = content.replace("article_type:", f"article_type: {args.type}", 1)
content = content.replace("priority:", f"priority: {args.priority}", 1)

out = root / "jobs" / f"{job_id}.md"
out.parent.mkdir(parents=True, exist_ok=True)
if out.exists():
    raise SystemExit(f"Already exists: {out}")
out.write_text(content, encoding="utf-8")
print(out)
