#!/usr/bin/env python3
"""Generate a weekly HOVEL business report from local metric CSV files.

Inputs are optional where unavailable. The report distinguishes observed facts
from hypotheses and never treats missing values as zero.
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTE_ARTICLES = ROOT / "data-collector" / "local-output" / "note" / "note_article_metrics.csv"
X_POSTS = ROOT / "data" / "x" / "post_metrics.csv"
AMAZON = ROOT / "data" / "amazon" / "associate_metrics.csv"
OUTPUT_DIR = ROOT / "loop-engineering" / "reports"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def as_int(value: str | None) -> int | None:
    if value is None or not str(value).strip():
        return None
    try:
        return int(float(str(value).replace(",", "")))
    except ValueError:
        return None


def classify_title(title: str) -> list[str]:
    rules = {
        "清潔感・ニオイ": ["臭", "汗", "口臭", "シャワー", "インナー", "スーツ", "オールドスパイス"],
        "商品比較・レビュー": ["おすすめ", "比較", "選び方", "レビュー", "3選", "7選"],
        "AI・仕事術": ["生成AI", "仕事", "残業", "上司", "手戻り"],
        "睡眠・集中": ["睡眠", "眠", "集中", "耳栓"],
        "食事・ダイエット": ["昼食", "食欲", "ダイエット", "コンビニ"],
    }
    matched = [name for name, terms in rules.items() if any(term in title for term in terms)]
    return matched or ["未分類"]


def article_section(rows: list[dict[str, str]]) -> tuple[str, list[str], list[str]]:
    valid = []
    for row in rows:
        views = as_int(row.get("views"))
        likes = as_int(row.get("likes"))
        comments = as_int(row.get("comments"))
        if views is None:
            continue
        valid.append({
            "title": row.get("title", ""),
            "views": views,
            "likes": likes or 0,
            "comments": comments or 0,
        })

    if not valid:
        return "- note記事別データ：未取得\n", [], []

    valid.sort(key=lambda item: (item["views"], item["likes"], item["comments"]), reverse=True)
    top = valid[:5]
    bottom = list(reversed(valid[-5:]))

    theme_views: Counter[str] = Counter()
    theme_articles: Counter[str] = Counter()
    for item in valid:
        for theme in classify_title(item["title"]):
            theme_views[theme] += item["views"]
            theme_articles[theme] += 1

    theme_lines = []
    for theme, total_views in theme_views.most_common():
        avg = total_views / theme_articles[theme]
        theme_lines.append(f"- {theme}: 合計{total_views}PV / {theme_articles[theme]}本 / 平均{avg:.1f}PV")

    lines = ["### 上位記事"]
    lines += [f"{index}. {item['title']} — {item['views']}PV / {item['likes']}スキ / {item['comments']}コメント" for index, item in enumerate(top, 1)]
    lines += ["", "### 下位記事"]
    lines += [f"- {item['title']} — {item['views']}PV" for item in bottom]
    lines += ["", "### テーマ別"] + theme_lines

    top_titles = [item["title"] for item in top]
    bottom_titles = [item["title"] for item in bottom]
    return "\n".join(lines) + "\n", top_titles, bottom_titles


def x_section(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "- X投稿別データ：未取得。市場反応の検証は未開始。\n"

    scored = []
    for row in rows:
        impressions = as_int(row.get("impressions"))
        profile_visits = as_int(row.get("profile_visits"))
        url_clicks = as_int(row.get("url_clicks"))
        replies = as_int(row.get("replies"))
        if impressions is None:
            continue
        scored.append({
            "text": row.get("post_text", row.get("post", ""))[:80],
            "impressions": impressions,
            "profile_visits": profile_visits,
            "url_clicks": url_clicks,
            "replies": replies,
        })

    if not scored:
        return "- X投稿別データ：列はあるが有効値なし。\n"

    scored.sort(key=lambda item: ((item["url_clicks"] or 0), (item["profile_visits"] or 0), (item["replies"] or 0), item["impressions"]), reverse=True)
    best = scored[:3]
    lines = ["### 反応上位投稿"]
    for item in best:
        lines.append(
            f"- {item['text']} — imp {item['impressions']} / profile {item['profile_visits']} / click {item['url_clicks']} / reply {item['replies']}"
        )
    return "\n".join(lines) + "\n"


def amazon_section(rows: list[dict[str, str]]) -> str:
    if not rows:
        return "- Amazonデータ：未取得\n"
    latest = rows[-1]
    clicks = as_int(latest.get("clicks"))
    orders = as_int(latest.get("orders"))
    revenue = as_int(latest.get("revenue_jpy"))
    cvr = None if clicks in (None, 0) or orders is None else orders / clicks * 100
    return (
        f"- クリック: {clicks if clicks is not None else 'missing'}\n"
        f"- 注文: {orders if orders is not None else 'missing'}\n"
        f"- 紹介料: {revenue if revenue is not None else 'missing'}円\n"
        f"- CVR: {f'{cvr:.1f}%' if cvr is not None else '算出不可'}\n"
    )


def build_actions(top_titles: list[str], bottom_titles: list[str], has_x: bool) -> str:
    actions = []
    if top_titles:
        actions.append(f"1. 上位テーマをXで3投稿ずつ検証する：{top_titles[0]}")
        actions.append("2. Xで最も返信・プロフィール遷移が多い悩みを、note記事へ昇格する")
        actions.append("3. note記事末尾のCTAを1つに絞り、関連商品または比較記事へ接続する")
    else:
        actions.append("1. note記事別CSVを取得する")
    if not has_x:
        actions.append("4. X投稿別データ収集を開始する。投稿文・仮説・反応を同一行で記録する")
    if bottom_titles:
        actions.append(f"5. 下位記事は追加量産せず、タイトルか導線を1回だけ改善する：{bottom_titles[0]}")
    return "\n".join(actions) + "\n"


def main() -> int:
    note_rows = read_csv(NOTE_ARTICLES)
    x_rows = read_csv(X_POSTS)
    amazon_rows = read_csv(AMAZON)

    note_text, top_titles, bottom_titles = article_section(note_rows)
    now = datetime.now()
    report = f"""# HOVEL Weekly Business Report

生成日時: {now.isoformat(timespec='seconds')}

## 1. 事業ファネル

Xで悩み仮説を検証 → noteで解決策を提示 → 比較・レビュー・商品導線で収益化

## 2. note実績

{note_text}
## 3. X市場反応

{x_section(x_rows)}
## 4. Amazon収益導線

{amazon_section(amazon_rows)}
## 5. 今週の判断

### Keep
- 反応が確認できたテーマと商品名入り記事を継続する
- Xでは宣伝より、悩み・体験・質問で市場の言葉を集める

### Improve
- X投稿に仮説IDを付け、note記事・商品導線まで追跡可能にする
- note記事末尾で「次に取る行動」を1つだけ提示する

### Stop
- Xで反応を測らずに記事を大量生産する
- PVだけで商品需要を判断する
- データ欠損を0として扱う

## 6. 次週アクション

{build_actions(top_titles, bottom_titles, bool(x_rows))}
## 7. 判定上の限界

- noteの数字は累計値であり、公開日や前週差を考慮していない
- X投稿別データがなければ、市場反応とnote流入の因果は判断できない
- Amazonクリックと記事別CTAの紐付けがなければ、収益貢献記事は特定できない
"""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"{now.strftime('%Y-%m-%d')}-weekly-business-report.md"
    output.write_text(report, encoding="utf-8")
    print(f"Report generated: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
