from .base import BaseAgent
class WriterAgent(BaseAgent):
    name="writer"
    def run(self,topic,inputs):
        return '---\ntitle: "{topic}｜会社員が最初に確認すべきこと"\nstatus: draft\nreviewed: false\n---\n\n# {topic}｜会社員が最初に確認すべきこと\n\n{topic}で困ったときは、対策を増やす前に状況を切り分けることが重要です。\n\n## 結論\n発生する時間帯、頻度、直前の行動、睡眠、食事、作業環境を記録し、影響が大きく変更しやすい要因から一つずつ見直します。\n\n## 最初に記録する項目\n- 発生した時刻\n- 前夜の睡眠時間\n- 食事の時間と量\n- カフェイン摂取\n- 直前の仕事\n\n## 注意点\n強い症状が続く場合は医療機関へ相談してください。'.format(topic=topic)
