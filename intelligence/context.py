from dataclasses import dataclass, asdict
from pathlib import Path
from .search import KnowledgeSearch
from .articles import ArticleIndex
from .prompts import PromptEngine

@dataclass
class IntelligenceContext:
    topic: str
    knowledge_results: list
    related_articles: list
    cannibalization_risks: list
    internal_link_candidates: list
    prompt_version: str = "v1"

    def to_dict(self):
        return asdict(self)

class IntelligenceLayer:
    def __init__(self, repo_root):
        self.repo_root = Path(repo_root)
        self.searcher = KnowledgeSearch([
            self.repo_root / "knowledge",
            self.repo_root / "company",
            self.repo_root / "os",
        ])
        self.article_index = ArticleIndex([
            self.repo_root / "content",
            self.repo_root / "articles",
            self.repo_root / "published",
        ])
        self.prompts = PromptEngine(self.repo_root / "prompts")

    def build_context(self, topic):
        self.article_index.build()
        knowledge = [x.to_dict() for x in self.searcher.search(topic)]
        related = self.article_index.related(topic)
        risks = self.article_index.cannibalization(topic)
        links = [x for x in related if x not in risks][:5]
        return IntelligenceContext(
            topic=topic,
            knowledge_results=knowledge,
            related_articles=related,
            cannibalization_risks=risks,
            internal_link_candidates=links,
        )
