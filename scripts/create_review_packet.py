#!/usr/bin/env python3
"""Generate a review-ready article packet without paid APIs."""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\-ぁ-んァ-ヶ一-龠々ー]+", "-", value.strip().lower(), flags=re.UNICODE)
    return re.sub(r"-+", "-", value).strip("-")[:60] or "article"


def build_packet(topic: str, article_type: str, keyword: str) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return f"""---
topic: {topic}
primary_keyword: {keyword}
article_type: {article_type}
status: ai-work-required
created: {today}
paid_api: false
---

# HOVEL 記事制作パケット

## 1. 制作条件

- テーマ: {topic}
- 主キーワード: {keyword}
- 記事種別: {article_type}
- 想定読者: 25〜30代の男性会社員
- 公開先: note
- 自動公開: 禁止
- 未使用商品の体験談: 禁止
- 医療・睡眠・食事の断定: 一次情報確認必須

## 2. ChatGPTへの実行指示

このファイルとリポジトリ内の `prompts/`、`config/`、既存記事を読み、次の順番で成果物を作成してください。

1. 市場調査
2. SEO設計
3. 投資審査
4. 商品選定（必要な場合のみ）
5. 記事執筆
6. ファクトチェック
7. 編集長審査

各工程の判断根拠を残し、最終稿だけでなく、修正必須事項も明示してください。

## 3. 必須成果物

- [ ] `market.md`
- [ ] `seo.md`
- [ ] `investment.md`
- [ ] `product.md` または商品導線不要の判断
- [ ] `draft.md`
- [ ] `factcheck.md`
- [ ] `editor.md`
- [ ] `publish-checklist.md`

## 4. 人間が確認する項目

- [ ] タイトルと検索意図が一致している
- [ ] 引用元を実際に開いて確認した
- [ ] 数値・価格・仕様・日付が最新である
- [ ] 未使用商品の使用感を書いていない
- [ ] 既存記事との重複がない
- [ ] 内部リンク先が正しい
- [ ] アフィリエイトリンクが正しい
- [ ] 誤字脱字とnote上の表示を確認した
- [ ] 公開を承認した

## 5. 完了条件

GitHub Actionsの品質検査が通り、編集長判定が `publishable` または `human-review` で、運営者が最終承認した状態。
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    parser.add_argument("--type", default="information", choices=["information", "comparison", "review", "pillar", "update"])
    parser.add_argument("--keyword")
    parser.add_argument("--repo-root", default=".")
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    slug = slugify(args.topic)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    packet_dir = root / "jobs" / f"{stamp}-{slug}"
    packet_dir.mkdir(parents=True, exist_ok=False)

    keyword = args.keyword or args.topic
    (packet_dir / "brief.md").write_text(build_packet(args.topic, args.type, keyword), encoding="utf-8")
    metadata = {
        "topic": args.topic,
        "primary_keyword": keyword,
        "article_type": args.type,
        "status": "ai-work-required",
        "paid_api": False,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (packet_dir / "job.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(packet_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
