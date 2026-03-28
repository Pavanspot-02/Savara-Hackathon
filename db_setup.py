import sqlite3
import json

# Your local database file
DB_NAME = "edtech_platform.db"

def get_db_connection():
    """Connects to the SQLite database and returns the connection object."""
    # Using check_same_thread=False is helpful for basic FastAPI setups 
    # during a hackathon, though in production you'd use connection pooling.
    conn = sqlite3.connect(DB_NAME, check_same_thread=False)
    conn.row_factory = sqlite3.Row # This lets you access columns by name (like a dictionary)
    return conn

def create_tables():
    """Creates the necessary tables based on the Phase 1 schema."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # 2. Notes Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS notes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        raw_text TEXT NOT NULL,
        summary TEXT,
        concepts TEXT, -- Storing JSON as text
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')

    # 3. Quiz Results Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        note_id INTEGER NOT NULL,
        score INTEGER,
        total_questions INTEGER,
        answers TEXT, -- Storing JSON as text
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (note_id) REFERENCES notes (id)
    )
    ''')

    # 4. Peer Matches Table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS peer_matches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id_1 INTEGER NOT NULL,
        user_id_2 INTEGER NOT NULL,
        shared_concepts TEXT, -- Storing JSON as text
        match_score REAL,
        FOREIGN KEY (user_id_1) REFERENCES users (id),
        FOREIGN KEY (user_id_2) REFERENCES users (id)
    )
    ''')

    conn.commit()
    conn.close()
    print(f"✅ Tables created successfully in {DB_NAME}!")

# --- DB Utility Functions (Insert / Query) ---

def insert_user(username, password_hash):
    """Utility to insert a new user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)", 
            (username, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return user_id
    except sqlite3.IntegrityError:
        print("User already exists!")
        return None
    finally:
        conn.close()

def get_user_by_username(username):
    """Utility to query a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    user = cursor.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    return dict(user) if user else None

if __name__ == "__main__":
    # Run this once to build the database
    create_tables()
    
    # Message for your teammate
    print(f"🚀 Database is live. Tell Pavan the connection string is simply: sqlite:///{DB_NAME}")