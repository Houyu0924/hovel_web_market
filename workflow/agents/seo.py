from .base import BaseAgent
class SeoAgent(BaseAgent):
    name="seo"
    def run(self,topic,inputs):
        return '# SEO設計: {topic}\n\n## Primary Keyword\n{topic}\n\n## Proposed Title\n{topic}｜会社員が最初に確認すべきこと\n\n## Search Intent\n原因、判断基準、具体策を知りたい。\n\n## 構成\n1. 結論\n2. 最初に確認すること\n3. 原因または選択基準\n4. 今日からの対策\n5. 注意点'.format(topic=topic)
