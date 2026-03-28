from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import sqlite3
import json

app = FastAPI(title="EdTech Platform API")

# --- Security & Config ---
SECRET_KEY = "super-secret-hackathon-key-change-this-later" # In prod, use env vars!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

DB_NAME = "edtech_platform.db"

def get_db():
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# --- Pydantic Models (For API Inputs) ---
class UserCreate(BaseModel):
    username: str
    password: str

class NoteCreate(BaseModel):
    raw_text: str
    summary: str
    concepts: dict  # Will be converted to JSON string

class QuizResultCreate(BaseModel):
    note_id: int
    score: int
    total_questions: int
    answers: dict

# --- CRUD Utilities ---
def get_user_by_username(db, username: str):
    return db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

# --- Auth Dependencies ---
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
    existing_user = get_user_by_username(db, user.username)
    if existing_user:
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
    cursor.execute(
        "INSERT INTO notes (user_id, raw_text, summary, concepts) VALUES (?, ?, ?, ?)",
        (current_user["id"], note.raw_text, note.summary, json.dumps(note.concepts))
    )
    db.commit()
    return {"message": "Note saved", "note_id": cursor.lastrowid}

@app.get("/notes/")
def get_notes_by_user(current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    notes = db.execute("SELECT * FROM notes WHERE user_id = ?", (current_user["id"],)).fetchall()
    return [dict(note) for note in notes]

@app.post("/quiz_results/")
def save_quiz_result(quiz: QuizResultCreate, current_user: dict = Depends(get_current_user), db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO quiz_results (user_id, note_id, score, total_questions, answers) VALUES (?, ?, ?, ?, ?)",
        (current_user["id"], quiz.note_id, quiz.score, quiz.total_questions, json.dumps(quiz.answers))
    )
    db.commit()
    return {"message": "Quiz result saved", "result_id": cursor.lastrowid}