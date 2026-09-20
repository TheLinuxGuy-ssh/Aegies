import sqlite3
from pathlib import Path

SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS problems(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        tags TEXT,
        box INTEGER NOT NULL,
        next_review TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS reviews(
        id INTEGER PRIMARY KEY,
        problem_id INTEGER NOT NULL,
        reviewed_at TEXT NOT NULL,
        result TEXT NOT NULL
    );
"""

def get_db_path() -> Path:
    config_dir = Path.home() / ".aegies"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "tracker.db"

class Database:
    def __init__(self, path):
        self.path = path
        
    def __enter__(self):
        self.conn = sqlite3.connect(self.path)
        return self.conn.cursor()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()

        self.conn.close()
        return False

def stream_problems(cur):
    cur.execute("SELECT id, title, difficulty, tags, box, next_review FROM problems")
    for row in cur:
        yield {
            "id": row[0],
            "title": row[1],
            "difficulty": row[2],
            "tags": row[3],
            "box": row[4],
            "next_review": row[5]
        }

def stream_reviews(cur):
    cur.execute("SELECT id, problem_id, reviewed_at, reviewed_at, result FROM reviews")
    for row in cur:
        yield {
            "id": row[0],
            "problem_id": row[1],
            "reviewed_at": row[2],
            "result": row[3],
        }