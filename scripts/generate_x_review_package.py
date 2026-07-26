#!/usr/bin/env python3
"""Create a free, review-ready X draft package from a Markdown article.

This script intentionally does not call a paid AI API. It extracts article metadata,
creates a structured review document, and embeds the repository prompt so a human can
paste the package into ChatGPT and return the result to `social/x/drafts/`.
"""

from __future__ import annotations

import re
import sys
from datetime import datetime, timezone
from pathlib import Path


MAX_EXCERPT_CHARS = 7000


def extract_title(markdown: str, fallback: str) -> str:
    frontmatter_match = re.search(r"^---\s*\n(.*?)\n---", markdown, re.DOTALL)
    if frontmatter_match:
        title_match = re.search(r"^title:\s*(.+)$", frontmatter_match.group(1), re.MULTILINE)
        if title_match:
            return title_match.group(1).strip().strip('"\'')

    heading_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()

    return fallback.replace("-", " ").strip().title()


def extract_summary(markdown: str) -> str:
    body = re.sub(r"^---\s*\n.*?\n---\s*", "", markdown, flags=re.DOTALL)
    paragraphs = []
    for block in re.split(r"\n\s*\n", body):
        cleaned = re.sub(r"^#{1,6}\s+", "", block.strip())
        cleaned = re.sub(r"[*_`>#-]", "", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()
        if len(cleaned) >= 40:
            paragraphs.append(cleaned)
        if len(paragraphs) == 2:
            break
    return " ".join(paragraphs)[:500]


def build_package(article_path: Path, output_path: Path) -> str:
    markdown = article_path.read_text(encoding="utf-8")
    slug = article_path.stem
    title = extract_title(markdown, slug)
    summary = extract_summary(markdown)
    generated_at = datetime.now(timezone.utc).isoformat()
    excerpt = markdown[:MAX_EXCERPT_CHARS]

    return f"""# X投稿レビュー・パッケージ

## メタデータ

- source_article: `{article_path.as_posix()}`
- slug: `{slug}`
- title: {title}
- generated_at: {generated_at}
- status: `needs-ai-generation`
- cost_mode: `free-manual-ai`

## 記事要約

{summary or '要約を自動抽出できませんでした。本文を参照してください。'}

## 作業手順

1. 下記の「生成指示」と「記事本文」をChatGPTへ貼り付ける
2. X投稿案5本をJSON形式で生成する
3. 内容を確認し、`social/x/drafts/{slug}.json` として保存する
4. 誇張、断定、根拠の不明な数値、140文字超過がないか確認する
5. 承認後、Xの予約投稿画面へ手動で登録する

この運用ではOpenAI APIとX APIを使用しないため、追加の従量課金は発生しません。

## 生成指示

あなたはHOVEL専属のSNS編集者です。
以下の記事をもとに、X投稿案を5本作成してください。

### 投稿タイプ

1. 公開告知
2. 記事の結論
3. 根拠・データ
4. 今日からできる行動
5. 数日後の再投稿

### 必須条件

- 各投稿は原則140文字以内
- 1投稿1メッセージ
- 誇張、煽り、根拠のない断定は禁止
- 科学的知見とHOVEL独自の提案を区別する
- URLは公開告知と再投稿の最大2本だけに含める
- ハッシュタグは原則0〜2個
- 読者は25〜35歳の男性会社員
- ダウナー寄りで落ち着いた、実務的な文体
- 出力はJSONのみ

### JSON形式

```json
{{
  "source_article": "{article_path.as_posix()}",
  "slug": "{slug}",
  "title": "{title}",
  "status": "draft",
  "posts": [
    {{
      "type": "announcement",
      "text": "",
      "url_required": true,
      "review_status": "pending"
    }}
  ]
}}
```

## 記事本文

```markdown
{excerpt}
```
"""


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: generate_x_review_package.py ARTICLE_PATH OUTPUT_PATH", file=sys.stderr)
        return 2

    article_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2])

    if not article_path.is_file():
        print(f"Article not found: {article_path}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_package(article_path, output_path), encoding="utf-8")
    print(f"Generated: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
