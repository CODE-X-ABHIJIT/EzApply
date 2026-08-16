import sqlite3
from datetime import datetime
from .config import DB_FILE


def connect():
    DB_FILE.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS jobs ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT,"
            "post_hash TEXT UNIQUE NOT NULL,"
            "post_text TEXT NOT NULL,"
            "recruiter_name TEXT, email TEXT, company TEXT, role TEXT,"
            "location TEXT, experience TEXT, match_score INTEGER DEFAULT 0,"
            "matched_keywords TEXT, subject TEXT, body TEXT,"
            "status TEXT DEFAULT 'pending', created_at TEXT NOT NULL, sent_at TEXT)"
        )


def add_job(job):
    with connect() as conn:
        cur = conn.execute(
            "INSERT OR IGNORE INTO jobs "
            "(post_hash,post_text,recruiter_name,email,company,role,location,"
            "experience,match_score,matched_keywords,subject,body,status,created_at) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (
                job["post_hash"], job["post_text"], job["recruiter_name"],
                job["email"], job["company"], job["role"], job["location"],
                job["experience"], job["match_score"], job["matched_keywords"],
                job["subject"], job["body"], "pending",
                datetime.now().isoformat(timespec="seconds"),
            ),
        )
        return cur.lastrowid


def get_job(job_id):
    with connect() as conn:
        return conn.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()


def pending_jobs():
    with connect() as conn:
        return conn.execute(
            "SELECT * FROM jobs WHERE status='pending' "
            "ORDER BY match_score DESC,id DESC"
        ).fetchall()


def email_already_sent(email):
    with connect() as conn:
        return conn.execute(
            "SELECT 1 FROM jobs WHERE lower(email)=lower(?) AND status='sent' LIMIT 1",
            (email,),
        ).fetchone() is not None


def mark_sent(job_id):
    with connect() as conn:
        conn.execute(
            "UPDATE jobs SET status='sent',sent_at=? WHERE id=?",
            (datetime.now().isoformat(timespec="seconds"), job_id),
        )


def mark_rejected(job_id):
    with connect() as conn:
        conn.execute("UPDATE jobs SET status='rejected' WHERE id=?", (job_id,))
