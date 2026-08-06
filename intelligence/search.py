from dataclasses import dataclass, asdict
from pathlib import Path
from .tokenize import token_set

TEXT_EXTENSIONS = {".md", ".txt", ".json", ".yaml", ".yml"}

@dataclass
class SearchResult:
    path: str
    score: float
    matched_terms: list
    excerpt: str

    def to_dict(self):
        return asdict(self)

def excerpt(text, terms, width=260):
    low = text.lower()
    positions = [low.find(t.lower()) for t in terms if low.find(t.lower()) >= 0]
    start = max(0, (min(positions) if positions else 0) - 80)
    return " ".join(text[start:start + width].split())

class KnowledgeSearch:
    def __init__(self, roots):
        self.roots = [Path(r) for r in roots]

    def files(self):
        for root in self.roots:
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in TEXT_EXTENSIONS:
                    yield path

    def search(self, query, limit=8):
        q = token_set(query)
        results = []
        if not q:
            return results

        for path in self.files():
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            doc = token_set(text + " " + path.stem.replace("-", " "))
            matched = sorted(q & doc)
            if not matched:
                continue
            score = len(matched) / max(1, len(q))
            score += min(0.25, len(matched) * 0.03)
            results.append(SearchResult(
                path=str(path),
                score=round(score, 4),
                matched_terms=matched,
                excerpt=excerpt(text, matched),
            ))
        return sorted(results, key=lambda x: (-x.score, x.path))[:limit]
