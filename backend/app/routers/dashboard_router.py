from fastapi import APIRouter, Depends
from app.auth import get_current_user
from app.db.database import get_user_stats

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("")
def dashboard(user: dict = Depends(get_current_user)):
    return {"username": user["username"], **get_user_stats(user["id"])}