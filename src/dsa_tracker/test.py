from db import Database, SCHEMA_SQL

with Database("tracker.db") as cur:
    cur.execute(SCHEMA_SQL)