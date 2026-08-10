from pathlib import Path
import tempfile
import unittest

from scripts.create_review_packet import build_packet, slugify
from scripts.quality_gate import inspect


class FreeMarketingSystemTest(unittest.TestCase):
    def test_slugify_supports_japanese(self):
        self.assertEqual(slugify("仕事中に眠すぎる"), "仕事中に眠すぎる")

    def test_packet_disables_paid_api(self):
        packet = build_packet("会社員向け耳栓", "comparison", "耳栓 会社員")
        self.assertIn("paid_api: false", packet)
        self.assertIn("自動公開: 禁止", packet)
        self.assertIn("未使用商品の体験談: 禁止", packet)

    def test_quality_gate_accepts_minimum_article(self):
        body = """---
title: テスト記事
status: draft
reviewed: false
---
# テスト記事

## 結論
""" + ("会社員が状況を記録し、変更しやすい要因から確認します。" * 40) + """

## 注意点
個別の症状については専門家へ相談してください。
"""
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.md"
            path.write_text(body, encoding="utf-8")
            self.assertEqual(inspect(path), [])

    def test_quality_gate_rejects_risky_claims(self):
        body = """---
title: テスト記事
status: draft
reviewed: false
---
# テスト
## 結論
絶対に治る方法です。
## 詳細
""" + ("説明文です。" * 100)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "article.md"
            path.write_text(body, encoding="utf-8")
            errors = inspect(path)
            self.assertTrue(any("guarantee" in error for error in errors))
            self.assertTrue(any("medical_claim" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
