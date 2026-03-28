from fastapi import APIRouter, Depends
from app.schemas import PeerResponse
from app.auth import get_current_user
from app.db.database import get_notes_by_user, get_all_notes_with_users
from app.services.peer_matcher import find_peers

router = APIRouter(prefix="/api/peers", tags=["peers"])


@router.get("", response_model=PeerResponse)
async def get_peers(user: dict = Depends(get_current_user)):
    my_notes = get_notes_by_user(user["id"])
    all_notes = get_all_notes_with_users()

    my_concepts = set()
    for note in my_notes:
        for c in note.get("concepts", []):
            my_concepts.add(c["name"] if isinstance(c, dict) else str(c))

    if not my_concepts:
        return PeerResponse(matches=[])

    return PeerResponse(matches=find_peers(user["id"], my_concepts, all_notes))