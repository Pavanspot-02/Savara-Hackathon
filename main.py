from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import sqlite3
import json
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(title="EdTech Platform API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows Soham's frontend to connect without getting blocked
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)
# --- Security & Config ---
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-for-dev")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DB_NAME = os.getenv("DATABASE_URL", "edtech_platform.db").replace("sqlite:///", "")

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# --- Pydantic Models ---
class UserCreate(BaseModel):
    username: str
    password: str

class NoteCreate(BaseModel):
    raw_text: str
    summary: Optional[str] = None
    concepts: Optional[Dict[str, str]] = None 

class QuizResultCreate(BaseModel):
    note_id: int
    score: float
    total_questions: int
    answers: Dict

# --- Auth Utilities ---
def get_user_by_username(db, username: str):
    return db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: sqlite3.Connection = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return dict(user)

# --- API Routes ---

@app.post("/signup")
def create_user(user: UserCreate, db: sqlite3.Connection = Depends(get_db)):
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = pwd_context.hash(user.password)
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (user.username, hashed_password))
    db.commit()
    return {"message": "User created successfully", "user_id": cursor.lastrowid}

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: sqlite3.Connection = Depends(get_db)):
    user = get_user_by_username(db, form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user["username"]})
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/notes/")
def save_note(note: NoteCreate, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    concepts_json = json.dumps(note.concepts) if note.concepts else None
    cursor.execute(
        "INSERT INTO notes (user_id, raw_text, summary, concepts) VALUES (?, ?, ?, ?)",
        (current_user["id"], note.raw_text, note.summary, concepts_json)
    )
    db.commit()
    return {"message": "Note saved", "note_id": cursor.lastrowid}

@app.get("/notes/")
def get_notes(current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, raw_text, summary, concepts FROM notes WHERE user_id = ?", (current_user["id"],))
    rows = cursor.fetchall()
    return [
        {
            "id": row["id"], 
            "raw_text": row["raw_text"], 
            "summary": row["summary"], 
            "concepts": json.loads(row["concepts"]) if row["concepts"] else {}
        } for row in rows
    ]

@app.post("/quiz_results/")
def save_quiz_result(quiz: QuizResultCreate, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO quiz_results (user_id, note_id, score, total_questions, answers) VALUES (?, ?, ?, ?, ?)",
        (current_user["id"], quiz.note_id, quiz.score, quiz.total_questions, json.dumps(quiz.answers))
    )
    db.commit()
    return {"message": "Quiz result saved", "result_id": cursor.lastrowid}