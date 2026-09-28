import sqlite3, os
from config import DATABASE_PATH

def connect():
    os.makedirs(os.path.dirname(DATABASE_PATH) or ".", exist_ok=True)
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    with connect() as db:
        db.execute("""CREATE TABLE IF NOT EXISTS experiences (
            experience_id TEXT PRIMARY KEY, experience_type TEXT NOT NULL, title TEXT NOT NULL,
            situation TEXT NOT NULL, context TEXT, action_taken TEXT, reason_for_action TEXT,
            outcome TEXT NOT NULL, success_or_failure TEXT NOT NULL, root_cause TEXT,
            lesson_learned TEXT NOT NULL, challenges TEXT, department TEXT, author TEXT,
            verification_status TEXT, hindsight_memory_id TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )""")

def create_experience(r):
    with connect() as db:
        db.execute("""INSERT INTO experiences
        (experience_id,experience_type,title,situation,context,action_taken,reason_for_action,outcome,
        success_or_failure,root_cause,lesson_learned,challenges,department,author,verification_status)
        VALUES (:experience_id,:experience_type,:title,:situation,:context,:action_taken,:reason_for_action,
        :outcome,:success_or_failure,:root_cause,:lesson_learned,:challenges,:department,:author,:verification_status)""", r)

def get_stats():
    with connect() as db:
        row=db.execute("""SELECT COUNT(*) total,
        SUM(CASE WHEN verification_status='Human-Verified Experience' THEN 1 ELSE 0 END) verified,
        SUM(CASE WHEN success_or_failure='Successful' THEN 1 ELSE 0 END) successful,
        SUM(CASE WHEN success_or_failure='Failed' THEN 1 ELSE 0 END) failed FROM experiences""").fetchone()
        return dict(row)

def get_recent():
    with connect() as db:
        return [dict(r) for r in db.execute("SELECT * FROM experiences ORDER BY created_at DESC LIMIT 6")]
