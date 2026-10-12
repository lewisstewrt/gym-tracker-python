import sqlite3

DB_PATH = "gym.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS exercises (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE COLLATE NOCASE
);

CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY,
    started_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sets (
    id           INTEGER PRIMARY KEY,
    session_id   INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    exercise_id  INTEGER NOT NULL REFERENCES exercises(id),
    set_number   INTEGER NOT NULL,
    reps         INTEGER NOT NULL CHECK (reps > 0),
    weight_kg    REAL    NOT NULL CHECK (weight_kg >= 0)
);
"""

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    with get_connection() as conn:
        conn.executescript(SCHEMA)

def get_or_create_exercise(conn, name):
    name = name.strip().lower()
    row = conn.execute(
        "SELECT id FROM exercises WHERE name =?", (name,)).fetchone()
    if row:
        return row["id"]

    cur = conn.execute("INSERT INTO exercises (name) VALUES (?)", (name,))
    return cur.lastrowid

def create_session(conn, started_at):
    cur = conn.execute("INSERT INTO sessions (started_at) VALUES (?)", (started_at,))
    return cur.lastrowid

def add_set(conn, session_id, exercise_id, set_number, reps, weight_kg):
    cur = conn.execute(
        "INSERT INTO sets (session_id, exercise_id, set_number, reps, weight_kg) VALUES (?, ?, ?, ?, ?)",
        (session_id, exercise_id, set_number, reps, weight_kg),
    )
    return cur.lastrowid


if __name__ == "__main__":
    create_tables()
    print("Database ready.")