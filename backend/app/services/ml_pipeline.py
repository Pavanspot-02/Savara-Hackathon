import re
from collections import Counter

_keybert_model = None

def _load_keybert():
    global _keybert_model
    if _keybert_model is not None:
        return _keybert_model
    try:
        from keybert import KeyBERT
        _keybert_model = KeyBERT("all-MiniLM-L6-v2")
        print("[ML] KeyBERT loaded.")
        return _keybert_model
    except Exception as e:
        print(f"[ML] KeyBERT not available: {e}")
        return None

def _stopwords():
    return {"the","a","an","is","are","was","were","be","been","being","have","has",
        "had","do","does","did","will","would","could","should","may","might","can",
        "need","to","of","in","for","on","with","at","by","from","as","into","through",
        "during","before","after","above","below","between","out","off","over","under",
        "again","further","then","once","here","there","when","where","why","how","all",
        "both","each","few","more","most","other","some","such","no","nor","not","only",
        "own","same","so","than","too","very","just","because","but","and","or","if",
        "while","that","this","these","those","it","its","he","she","they","them","we",
        "you","i","which","what","who","also","about","up","one","two"}

def _summarize(text, ratio=0.35):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    if len(sentences) <= 3:
        return text.strip()

    stops = _stopwords()
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    freq = Counter(w for w in words if w not in stops)
    mx = max(freq.values()) if freq else 1
    for w in freq:
        freq[w] /= mx

    scored = []
    for i, s in enumerate(sentences):
        sw = re.findall(r'\b[a-zA-Z]{3,}\b', s.lower())
        if not sw:
            continue
        score = sum(freq.get(w, 0) for w in sw) / len(sw) + 1.0 / (i + 1) * 0.3
        scored.append((score, i, s))

    scored.sort(reverse=True)
    top_n = max(3, int(len(sentences) * ratio))
    selected = sorted(scored[:top_n], key=lambda x: x[1])
    return " ".join(s for _, _, s in selected)

def _fallback_concepts(text):
    stops = _stopwords()
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    freq = Counter(w for w in words if w not in stops)

    wl = text.lower().split()
    bigrams = []
    for i in range(len(wl) - 1):
        w1 = re.sub(r'[^a-z]', '', wl[i])
        w2 = re.sub(r'[^a-z]', '', wl[i + 1])
        if w1 not in stops and w2 not in stops and len(w1) > 2 and len(w2) > 2:
            bigrams.append(f"{w1} {w2}")

    bf = Counter(bigrams)
    mx = max(freq.values()) if freq else 1
    concepts = [{"name": p, "score": round(min(c / mx + 0.3, 1.0), 2)} for p, c in bf.most_common(5)]
    for w, c in freq.most_common(10):
        if any(w in x["name"] for x in concepts):
            continue
        concepts.append({"name": w, "score": round(c / mx, 2)})
        if len(concepts) >= 8:
            break
    return concepts[:8]

async def run_pipeline(raw_text):
    summary = _summarize(raw_text)

    model = _load_keybert()
    if model:
        try:
            kw = model.extract_keywords(
                raw_text,
                keyphrase_ngram_range=(1, 2),
                stop_words="english",
                top_n=8,
                use_mmr=True,
                diversity=0.5,
            )
            concepts = [{"name": k, "score": round(s, 3)} for k, s in kw if s >= 0.1]
            if concepts:
                return {"summary": summary, "concepts": concepts}
        except:
            pass

    return {"summary": summary, "concepts": _fallback_concepts(raw_text)}