from collections import defaultdict
from app.schemas import PeerMatch


def find_peers(current_user_id, my_concepts, all_notes, top_k=5):
    user_concepts = defaultdict(lambda: {"concepts": set(), "username": ""})

    for note in all_notes:
        uid = note["user_id"]
        if uid == current_user_id:
            continue
        user_concepts[uid]["username"] = note.get("username", f"User_{uid}")
        for c in note.get("concepts", []):
            name = c["name"] if isinstance(c, dict) else str(c)
            user_concepts[uid]["concepts"].add(name.lower())

    my_lower = {c.lower() for c in my_concepts}
    matches = []

    for uid, data in user_concepts.items():
        intersection = my_lower & data["concepts"]
        if not intersection:
            continue
        union = my_lower | data["concepts"]
        score = len(intersection) / len(union) if union else 0

        matches.append(PeerMatch(
            user_id=uid,
            username=data["username"],
            shared_concepts=sorted(intersection),
            match_score=round(score, 2),
        ))

    matches.sort(key=lambda m: m.match_score, reverse=True)
    return matches[:top_k]