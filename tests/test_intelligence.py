import tempfile
import unittest
from pathlib import Path

from intelligence.search import KnowledgeSearch
from intelligence.articles import ArticleIndex
from intelligence.prompts import PromptEngine

class IntelligenceTests(unittest.TestCase):
    def test_search(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "knowledge").mkdir()
            (root / "knowledge" / "sleep.md").write_text("会社員の睡眠と仕事中の眠気", encoding="utf-8")
            results = KnowledgeSearch([root / "knowledge"]).search("会社員 睡眠")
            self.assertTrue(results)
            self.assertIn("会社員", results[0].matched_terms)

    def test_article_similarity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            root.mkdir(exist_ok=True)
            (root / "a.md").write_text("# 仕事中に眠い人の睡眠対策", encoding="utf-8")
            idx = ArticleIndex([root])
            idx.build()
            self.assertTrue(idx.related("仕事中 眠い 睡眠"))

    def test_prompt_render(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "market.md").write_text("Topic={{topic}}", encoding="utf-8")
            rendered = PromptEngine(root).render("market", {"topic": "睡眠"})
            self.assertEqual(rendered, "Topic=睡眠")

if __name__ == "__main__":
    unittest.main()
