from .base import BaseAgent
class InvestmentAgent(BaseAgent):
    name="investment"
    def run(self,topic,inputs):
        return '# 投資審査: {topic}\n\n## 判定\n条件付き承認\n\n## 条件\n- 既存記事と重複しない\n- 読者が実行できる具体策がある\n- 根拠のない断定をしない\n- 無理な商品導線を置かない'.format(topic=topic)
