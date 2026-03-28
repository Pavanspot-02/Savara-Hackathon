import sqlite3, json, os
from contextlib import contextmanager
from app.config import DATABASE_PATH

def get_db_path():
    os.makedirs(os.path.dirname(DATABASE_PATH) or "data", exist_ok=True)
    return DATABASE_PATH

def init_db():
    conn = sqlite3.connect(get_db_path())
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            raw_text TEXT NOT NULL,
            summary TEXT,
            concepts TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            note_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            answers TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (note_id) REFERENCES notes(id)
        );
    """)
    conn.commit()
    conn.close()

@contextmanager
def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def create_user(username, password_hash):
    with get_connection() as conn:
        return conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        ).lastrowid

def get_user_by_username(username):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username, password_hash FROM users WHERE username = ?",
            (username,)
        ).fetchone()
        return dict(row) if row else None

def get_user_by_id(user_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, username FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return dict(row) if row else None

def save_note(user_id, raw_text, summary=None, concepts=None):
    with get_connection() as conn:
        return conn.execute(
            "INSERT INTO notes (user_id, raw_text, summary, concepts) VALUES (?, ?, ?, ?)",
            (user_id, raw_text, summary, json.dumps(concepts or []))
        ).lastrowid

def update_note_ml(note_id, summary, concepts):
    with get_connection() as conn:
        conn.execute(
            "UPDATE notes SET summary = ?, concepts = ? WHERE id = ?",
            (summary, json.dumps(concepts), note_id)
        )

def get_note(note_id):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        if row:
            d = dict(row)
            d["concepts"] = json.loads(d["concepts"])
            return d
        return None

def get_notes_by_user(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM notes WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            d["concepts"] = json.loads(d["concepts"])
            results.append(d)
        return results

def get_all_notes_with_users():
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT n.*, u.username FROM notes n
            JOIN users u ON n.user_id = u.id
            WHERE n.concepts IS NOT NULL AND n.concepts != '[]'
        """).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            d["concepts"] = json.loads(d["concepts"])
            results.append(d)
        return results

def save_quiz_result(user_id, note_id, score, total, answers):
    with get_connection() as conn:
        return conn.execute(
            "INSERT INTO quiz_results (user_id, note_id, score, total_questions, answers) VALUES (?, ?, ?, ?, ?)",
            (user_id, note_id, score, total, json.dumps(answers))
        ).lastrowid

def get_quiz_results_by_user(user_id):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM quiz_results WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        ).fetchall()
        results = []
        for row in rows:
            d = dict(row)
            d["answers"] = json.loads(d["answers"])
            results.append(d)
        return results

def get_user_stats(user_id):
    with get_connection() as conn:
        nc = conn.execute("SELECT COUNT(*) FROM notes WHERE user_id = ?", (user_id,)).fetchone()[0]
        qc = conn.execute("SELECT COUNT(*) FROM quiz_results WHERE user_id = ?", (user_id,)).fetchone()[0]
        avg = conn.execute(
            "SELECT AVG(CAST(score AS FLOAT)/total_questions) FROM quiz_results WHERE user_id = ?",
            (user_id,)
        ).fetchone()
        return {
            "notes_uploaded": nc,
            "quizzes_taken": qc,
            "avg_score_pct": round((avg[0] or 0) * 100, 1)
        }