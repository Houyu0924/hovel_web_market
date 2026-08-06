from .base import BaseAgent

class MarketAgent(BaseAgent):
    name = "market"

    def run(self, topic, inputs):
        return f"""# 市場調査: {topic}

## Knowledge Base参照
{inputs.get("_knowledge_context", "- 該当なし")}

## 既存記事
{inputs.get("_related_articles", "- 該当なし")}

## 想定読者
25〜30代の男性会社員。

## 調査仮説
読者は原因、判断基準、具体策を求める。購入導線は問題解決に必要な場合のみ設計する。

## 次工程への条件
外部検索による検索需要・競合・最新情報の確認が必要。
"""
