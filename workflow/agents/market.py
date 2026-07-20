from .base import BaseAgent
class MarketAgent(BaseAgent):
    name="market"
    def run(self,topic,inputs):
        return '# 市場調査: {topic}\n\n## 想定読者\n25〜30代の男性会社員。\n\n## 読者課題\n- 何から確認すべきか分からない\n- 実行可能な判断基準が欲しい\n- 商品紹介より先に問題整理を求めている\n\n## 判断\n検索需要、競合、既存記事との重複を確認することを条件に次工程へ進める。'.format(topic=topic)
