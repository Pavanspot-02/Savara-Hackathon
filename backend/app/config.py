import os
from datetime import timedelta

SECRET_KEY = os.getenv("JWT_SECRET", "hackathon-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE = timedelta(hours=24)
DATABASE_PATH = os.getenv("DATABASE_PATH", "data/app.db")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
TROCR_MODEL = "microsoft/trocr-base-handwritten"