from .base import BaseAgent
class EditorAgent(BaseAgent):
    name="editor"
    def run(self,topic,inputs):
        return '# 編集長レビュー\n\n## 判定\nhuman-review\n\n## 公開前の必須修正\n1. テーマ固有の一次情報を追加\n2. 導入文を具体化\n3. 内部リンクを設定\n4. ファクトチェック指摘を解消\n5. CEOが最終承認\n\n## 公開状態\n自動公開は禁止。人間の最終確認待ち。'.format(topic=topic)
