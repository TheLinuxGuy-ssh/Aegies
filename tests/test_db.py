from db import Database, SCHEMA_SQL
from datetime import date, timedelta

# DB Tests

def test_add_problem_inserts_row(tmp_path):
    db_file = tmp_path / "test.db"
    with Database(str(db_file)) as cur:
        cur.executescript(SCHEMA_SQL)
        cur.execute(
            "INSERT INTO problems (title, difficulty, tags, box, next_review) VALUES(?, ?, ?, ?, ?)",
            ("Two Sum", "Easy", "", 1, "2026-09-24")
        )
    

    with Database(str(db_file)) as cur:
        cur.executescript(SCHEMA_SQL)
        cur.execute(
            "SELECT * FROM problems WHERE title = ?", ("Two Sum",)
        )
        row = cur.fetchone()

    assert row is not None
    assert row[1] == "Two Sum"

def test_rollback_on_bad_insert(tmp_path):
    db_file = tmp_path / "test.db"

    with Database(str(db_file)) as cur:
        cur.executescript(SCHEMA_SQL)
        cur.execute(
            "INSERT INTO problems (title, difficulty, tags, box, next_review) VALUES(?, ?, ?, ?, ?)",
            ("Two Sum", "Easy", "", 1, "2026-09-24")
        )

    try:
        with Database(str(db_file)) as cur:
            cur.execute(
                "INSERT INTO problems (tile, how) VALUES(?, ?)",
                ("Two Sum", "Easy")
            )
    except Exception:
        pass
    

    with Database(str(db_file)) as cur:
        cur.execute(
            "SELECT * FROM problems WHERE title = ?", ("Two Sum",)
        )
        row = cur.fetchall()

    assert row is not None
    assert len(row) == 1