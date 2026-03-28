from fastapi import APIRouter, HTTPException
from app.schemas import SignupRequest, LoginRequest, TokenResponse
from app.auth import hash_password, verify_password, create_token
from app.db.database import create_user, get_user_by_username

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/signup", response_model=TokenResponse)
def signup(req: SignupRequest):
    if get_user_by_username(req.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    user_id = create_user(req.username, hash_password(req.password))
    return TokenResponse(access_token=create_token(user_id))


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = get_user_by_username(req.username)
    if not user or not verify_password(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenResponse(access_token=create_token(user["id"]))