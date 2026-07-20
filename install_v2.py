#!/usr/bin/env python3
from pathlib import Path
import shutil
from datetime import datetime

SOURCE = Path(__file__).resolve().parent
REPO = Path.cwd()
BACKUP = REPO / ".hovel_backup_v2" / datetime.now().strftime("%Y%m%d_%H%M%S")

targets = [
    "docs/workflow.md",
    "docs/architecture.md",
    "docs/style-guide.md",
    "prompts/market_research.md",
    "prompts/seo.md",
    "prompts/investment.md",
    "prompts/product.md",
    "prompts/writer.md",
    "prompts/factcheck.md",
    "prompts/marketing.md",
    "prompts/editor.md",
    "ideas/backlog_v2.csv",
    "products/categories/eye-mask.csv",
    "keywords/body.csv",
    "data/affiliate.csv",
    "data/experiments.csv",
]

if not (REPO / ".git").exists():
    raise SystemExit("エラー: hovel_web_market のルートフォルダで実行してください。")

for rel in targets:
    src = SOURCE / rel
    dst = REPO / rel
    if dst.exists():
        backup_dst = BACKUP / rel
        backup_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, backup_dst)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"installed: {rel}")

print("\nHOVEL Repository v2 の配置が完了しました。")
if BACKUP.exists():
    print(f"既存ファイルのバックアップ: {BACKUP}")
print("GitHub Desktopで差分を確認し、commit / pushしてください。")
