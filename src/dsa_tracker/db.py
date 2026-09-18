import sqlite3

SCHEMA_SQL = """
    CREATE TABLE IF NOT EXISTS problems(
        id INTEGAR PRIMARY KEY,
        title TEXT NOT NULL
    )
"""

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