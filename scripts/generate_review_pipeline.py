#!/usr/bin/env python3
"""Generate HOVEL review assets from the product review database.

Reads data/product-reviews/product_review_db.csv and creates, for each review ID:
- a note article draft
- three X post drafts
- a compact comparison table
- a CTA block for Amazon or other affiliate links

The script does not publish content or call external APIs. It only creates local
Markdown files so the operator can review and edit them before publication.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "product-reviews" / "product_review_db.csv"
OUTPUT_ROOT = ROOT / "loop-engineering" / "review-pipeline-output"


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "review"


def value(row: dict[str, Any], *keys: str, default: str = "") -> str:
    for key in keys:
        raw = row.get(key)
        if raw is not None and str(raw).strip():
            return str(raw).strip()
    return default


def load_rows() -> list[dict[str, str]]:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Product review DB not found: {DB_PATH}")

    with DB_PATH.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def comparison_table(row: dict[str, str]) -> str:
    product = value(row, "product_name", "商品名", default="商品名未設定")
    rating = value(row, "hovel_rating", "HOVEL評価", default="未評価")
    verdict = value(row, "decision", "判定", default="保留")
    merits = value(row, "merits", "メリット", default="検証中")
    demerits = value(row, "demerits", "デメリット", default="検証中")

    return "\n".join(
        [
            "| 比較項目 | 評価 |",
            "|---|---|",
            f"| 商品 | {product} |",
            f"| HOVEL評価 | {rating} |",
            f"| 現時点の判定 | {verdict} |",
            f"| 主なメリット | {merits} |",
            f"| 主なデメリット | {demerits} |",
        ]
    )


def cta_block(row: dict[str, str]) -> str:
    product = value(row, "product_name", "商品名", default="この商品")
    affiliate_url = value(row, "affiliate_url", "Amazonリンク", "affiliate_link")
    decision = value(row, "decision", "判定", default="保留")

    if affiliate_url:
        return (
            f"## {product}を確認する\n\n"
            f"現時点のHOVEL判定は**{decision}**です。購入前に容量、価格、配送条件、"
            f"返品条件を商品ページで確認してください。\n\n"
            f"[Amazonで{product}を見る]({affiliate_url})\n\n"
            "※リンク先の価格や在庫は変更される場合があります。"
        )

    return (
        f"## {product}を検討する前に\n\n"
        f"現時点のHOVEL判定は**{decision}**です。アフィリエイトリンクは未設定です。"
        "レビューが十分に揃うまでは、購入を急がず比較を続けます。"
    )


def note_draft(row: dict[str, str]) -> str:
    review_id = value(row, "review_id", "レビューID", default="PR-UNKNOWN")
    product = value(row, "product_name", "商品名", default="商品名未設定")
    brand = value(row, "brand", "ブランド", default="")
    problem = value(row, "problem", "解決する悩み", default="読者の悩み")
    audience = value(row, "target_reader", "対象読者", default="25〜35歳の男性会社員")
    category = value(row, "category", "カテゴリ", default="商品レビュー")
    first_impression = value(row, "day1_review", "Day1レビュー", "first_impression", default="検証中")
    day7 = value(row, "day7_review", "Day7レビュー", default="未記録")
    day30 = value(row, "day30_review", "Day30レビュー", default="未記録")
    merits = value(row, "merits", "メリット", default="検証中")
    demerits = value(row, "demerits", "デメリット", default="検証中")
    verdict = value(row, "decision", "判定", default="保留")

    title = f"{product}は会社員に向いている？実際に使って分かったメリット・注意点"

    sections = [
        f"# {title}",
        "",
        f"レビューID：`{review_id}`  ",
        f"ブランド：{brand or '未設定'}  ",
        f"カテゴリ：{category}",
        "",
        "## 先に結論",
        "",
        f"{product}の現時点のHOVEL判定は**{verdict}**です。",
        f"対象は、{audience}のうち、**{problem}**で困っている人です。",
        "",
        "## この商品を検証する理由",
        "",
        f"今回確認したいのは、商品そのものの人気ではなく、{problem}という悩みに対して、"
        "会社員の日常で実用的な選択肢になるかどうかです。",
        "",
        "## Day1レビュー",
        "",
        first_impression,
        "",
        "## Day7レビュー",
        "",
        day7,
        "",
        "## Day30レビュー",
        "",
        day30,
        "",
        "## 良かった点",
        "",
        merits,
        "",
        "## 気になった点",
        "",
        demerits,
        "",
        "## 比較表",
        "",
        comparison_table(row),
        "",
        "## 向いている人・向いていない人",
        "",
        f"**向いている可能性がある人**：{problem}を具体的に改善したい人。",
        "",
        "**向いていない可能性がある人**：香り、価格、使用感などに強い制約があり、"
        "事前比較をせずに購入しようとしている人。",
        "",
        cta_block(row),
        "",
        "## HOVELのレビュー方針",
        "",
        "HOVELでは、公開情報だけで断定せず、実使用、読者反応、記事PV、クリック、成約の"
        "データを分けて記録します。評価は追加検証によって変更する場合があります。",
    ]

    return "\n".join(sections)


def x_posts(row: dict[str, str]) -> str:
    review_id = value(row, "review_id", "レビューID", default="PR-UNKNOWN")
    product = value(row, "product_name", "商品名", default="この商品")
    problem = value(row, "problem", "解決する悩み", default="仕事中の不快感")
    verdict = value(row, "decision", "判定", default="検証中")
    note_url = value(row, "note_url", "note記事", default="")

    link_line = f"\n{note_url}" if note_url else ""

    posts = [
        "# X投稿案",
        "",
        f"レビューID：`{review_id}`",
        "",
        "## 1. 悩み型",
        "",
        f"{problem}で困っていても、商品名から探し始めると選択を誤りやすいです。\n"
        "最初に確認したいのは、いつ、どこで、何が不快なのか。\n"
        "HOVELでは悩みを分解してから商品を検証します。",
        "",
        "## 2. 検証途中型",
        "",
        f"{product}を実際に検証しています。\n"
        f"現時点の判定は「{verdict}」。\n"
        "良い点だけでなく、会社員が使いにくい条件も記録します。"
        f"{link_line}",
        "",
        "## 3. 学び型",
        "",
        f"{problem}への対策は、商品を買う前に原因の優先順位を整理した方が失敗しにくいです。\n"
        f"今回の{product}レビューでも、誰に向くか、誰には向かないかを分けて検証しています。"
        f"{link_line}",
    ]

    return "\n".join(posts)


def write_assets(row: dict[str, str]) -> Path:
    review_id = value(row, "review_id", "レビューID", default="PR-UNKNOWN")
    product = value(row, "product_name", "商品名", default="review")
    directory = OUTPUT_ROOT / f"{review_id}-{slugify(product)}"
    directory.mkdir(parents=True, exist_ok=True)

    (directory / "note-draft.md").write_text(note_draft(row), encoding="utf-8")
    (directory / "x-posts.md").write_text(x_posts(row), encoding="utf-8")
    (directory / "comparison-table.md").write_text(comparison_table(row) + "\n", encoding="utf-8")
    (directory / "cta.md").write_text(cta_block(row) + "\n", encoding="utf-8")
    return directory


def main() -> int:
    try:
        rows = load_rows()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if not rows:
        print("ERROR: Product review DB has no rows.", file=sys.stderr)
        return 2

    generated: list[Path] = []
    for row in rows:
        review_id = value(row, "review_id", "レビューID")
        if not review_id:
            continue
        generated.append(write_assets(row))

    if not generated:
        print("ERROR: No valid review rows were found.", file=sys.stderr)
        return 3

    print(f"Generated review assets for {len(generated)} product(s).")
    for directory in generated:
        print(directory)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
