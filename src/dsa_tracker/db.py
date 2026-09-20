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