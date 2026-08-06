import re

STOPWORDS = {
    "こと","ため","について","から","まで","です","ます","する","した","して",
    "いる","ある","なる","その","この","そして","また","より","もの","よう",
    "the","and","for","with","that","this","from","into","your","you"
}

def normalize(text):
    return re.sub(r"\s+", " ", text.lower()).strip()

def _jp_ngrams(value):
    value = re.sub(r"[^ぁ-んァ-ヶ一-龠々ー]", "", value)
    result = []
    for n in (2, 3, 4):
        result.extend(value[i:i+n] for i in range(max(0, len(value)-n+1)))
    return result

def tokens(text):
    normalized = normalize(text)
    latin = re.findall(r"[a-z0-9_]+", normalized)
    jp_chunks = re.findall(r"[ぁ-んァ-ヶ一-龠々ー]+", normalized)
    result = [p for p in latin if p not in STOPWORDS and len(p) > 1]
    for chunk in jp_chunks:
        if chunk not in STOPWORDS and len(chunk) > 1:
            result.append(chunk)
        result.extend(_jp_ngrams(chunk))
    return result

def token_set(text):
    return set(tokens(text))
