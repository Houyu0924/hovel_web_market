import re
from dataclasses import dataclass, asdict
from pathlib import Path
from .tokenize import token_set

TITLE_PATTERNS = [
    re.compile(r'^title:\s*["\']?(.*?)["\']?\s*$', re.M),
    re.compile(r'^#\s+(.+?)\s*$', re.M),
]

@dataclass
class ArticleRecord:
    path: str
    title: str
    tokens: list

    def to_dict(self):
        return asdict(self)

def extract_title(text, fallback):
    for pattern in TITLE_PATTERNS:
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return fallback

class ArticleIndex:
    def __init__(self, roots):
        self.roots = [Path(r) for r in roots]
        self.records = []

    def build(self):
        self.records = []
        for root in self.roots:
            if not root.exists():
                continue
            for path in root.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                title = extract_title(text, path.stem)
                self.records.append(ArticleRecord(
                    path=str(path),
                    title=title,
                    tokens=sorted(token_set(title + " " + text[:1500])),
                ))
        return self.records

    @staticmethod
    def similarity(a, b):
        aa, bb = set(a), set(b)
        if not aa or not bb:
            return 0.0
        return len(aa & bb) / len(aa | bb)

    def related(self, topic, limit=8):
        q = token_set(topic)
        rows = []
        for record in self.records:
            score = self.similarity(q, record.tokens)
            if score > 0:
                rows.append({
                    "path": record.path,
                    "title": record.title,
                    "score": round(score, 4),
                })
        return sorted(rows, key=lambda x: (-x["score"], x["title"]))[:limit]

    def cannibalization(self, topic, threshold=0.22):
        return [x for x in self.related(topic, limit=20) if x["score"] >= threshold]
