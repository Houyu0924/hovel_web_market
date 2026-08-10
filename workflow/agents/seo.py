from .base import BaseAgent

class SeoAgent(BaseAgent):
    name = "seo"

    def run(self, topic, inputs):
        return f"""# SEO設計: {topic}

## Primary Keyword
{topic}

## Proposed Title
{topic}｜会社員が最初に確認すべきこと

## カニバリゼーション候補
{inputs.get("_cannibalization_risks", "- 該当なし")}

## 内部リンク候補
{inputs.get("_internal_links", "- 該当なし")}

## 構成
1. 結論
2. 状況の切り分け
3. 原因・比較軸
4. 実行手順
5. 注意点
6. 関連記事

## 判定
重複リスクがある場合は、新規記事ではなく既存記事更新も検討する。
"""
