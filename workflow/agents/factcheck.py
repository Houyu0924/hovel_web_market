from .base import BaseAgent
class FactCheckAgent(BaseAgent):
    name="factcheck"
    def run(self,topic,inputs):
        draft=inputs.get("draft.md","")
        flags=[x for x in ("絶対","必ず","確実に") if x in draft]
        prefix="\n".join(f"- 過度な断定表現を確認: {x}" for x in flags) or "- 自動検査で重大な断定表現は未検出"
        return prefix+"\n\n"+'# ファクトチェック結果\n\n## 判定\nrevision-required\n\n## 手動確認が必要\n- 健康・睡眠・食事に関する一次情報\n- 数値や期間\n- 医療表現\n- 内部リンク\n- 商品仕様と価格\n\n## 制約\nこのMVPは外部資料との照合を行わない。'
