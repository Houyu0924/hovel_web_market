from .base import BaseAgent
class ProductAgent(BaseAgent):
    name="product"
    def run(self,topic,inputs):
        return '# 商品機会調査: {topic}\n\n## 判断\n現時点では具体商品を自動選定しない。\n\n## 掲載条件\n- メーカー公式仕様を確認\n- 最新価格を確認\n- 未使用なら使用感を書かない\n- 比較軸を明示'.format(topic=topic)
