import json, re, httpx
from app.config import CLAUDE_API_KEY
from app.schemas import QuizQuestion, QuizOption


async def generate_quiz(summary, raw_text):
    if CLAUDE_API_KEY:
        try:
            return await _claude_gen(summary, raw_text)
        except Exception as e:
            print(f"[Quiz] Claude failed: {e}")
    return _fallback(summary, raw_text)


async def _claude_gen(summary, raw_text):
    prompt = (
        "Generate exactly 5 MCQs from these notes. Mix difficulty: 2 easy, 2 medium, 1 hard. "
        "Return ONLY a JSON array:\n"
        '[{"question": "...", "options": {"A": "...", "B": "...", "C": "...", "D": "..."}, "correct": "A"}]\n\n'
        f"SUMMARY: {summary[:1000]}\nNOTES: {raw_text[:1500]}"
    )
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": CLAUDE_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1500,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        r.raise_for_status()

    text = re.sub(r'```json\s*|```\s*', '', r.json()["content"][0]["text"])
    data = json.loads(text.strip())
    return [
        QuizQuestion(
            id=i + 1,
            question=q["question"],
            options=[QuizOption(label=l, text=t) for l, t in q["options"].items()],
            correct=q["correct"],
        )
        for i, q in enumerate(data[:5])
    ]


def _fallback(summary, raw_text):
    full = summary + " " + raw_text
    sents = [s for s in re.split(r'(?<=[.!?])\s+', full.strip()) if 6 <= len(s.split()) < 40]

    stops = {
        "the", "a", "an", "is", "are", "was", "were", "in", "on", "at", "to",
        "for", "of", "with", "and", "or", "but", "that", "this", "by", "from",
        "as", "it", "its", "be", "has", "have", "had", "not", "can", "will",
        "do", "does", "did", "may", "also", "more",
    }

    all_terms = list(set(
        t for t in re.findall(r'\b[A-Za-z]{4,}\b', full) if t.lower() not in stops
    ))

    qs, seen = [], set()
    for i, s in enumerate(sents[:7]):
        if len(qs) >= 5:
            break
        key = s.lower()[:50]
        if key in seen:
            continue
        seen.add(key)

        words = s.split()
        cands = [
            (j, w, re.sub(r'[^a-zA-Z]', '', w))
            for j, w in enumerate(words)
            if re.sub(r'[^a-zA-Z]', '', w).lower() not in stops
            and len(re.sub(r'[^a-zA-Z]', '', w)) > 3
        ]
        if not cands:
            continue

        idx, _, ans = max(cands, key=lambda x: len(x[2]))
        wc = words.copy()
        wc[idx] = "________"

        dist = [t for t in all_terms if t.lower() != ans.lower()][:3]
        while len(dist) < 3:
            dist.append(f"option_{len(dist) + 1}")

        opts = [ans] + dist[:3]
        rot = (i * 7 + 3) % 4
        opts = opts[rot:] + opts[:rot]
        ci = opts.index(ans)
        labels = ["A", "B", "C", "D"]

        qs.append(QuizQuestion(
            id=len(qs) + 1,
            question="Fill in the blank: " + " ".join(wc),
            options=[QuizOption(label=labels[j], text=opts[j]) for j in range(4)],
            correct=labels[ci],
        ))

    while len(qs) < 3:
        qs.append(QuizQuestion(
            id=len(qs) + 1,
            question="What is the main topic of these notes?",
            options=[
                QuizOption(label="A", text="The concepts described"),
                QuizOption(label="B", text="An unrelated topic"),
                QuizOption(label="C", text="A math proof"),
                QuizOption(label="D", text="A recipe"),
            ],
            correct="A",
        ))

    return qs[:5]