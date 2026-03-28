from datetime import datetime, timezone
import hashlib, secrets
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE
from app.db.database import get_user_by_id

security = HTTPBearer()

def hash_password(password):
    salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${h}"

def verify_password(plain, hashed):
    salt, h = hashed.split("$", 1)
    return hashlib.sha256((salt + plain).encode()).hexdigest() == h

def create_token(user_id):
    expire = datetime.now(timezone.utc) + ACCESS_TOKEN_EXPIRE
    return jwt.encode({"sub": str(user_id), "exp": expire}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Invalid token")
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user