"""
Database Manager - AIChild
Handles all SQLite operations: conversations, knowledge, settings, backups
"""

import sqlite3
import json
import os
import datetime
from pathlib import Path


DB_PATH = Path(__file__).parent.parent / "data" / "aichild.db"
LOG_PATH = Path(__file__).parent.parent / "data" / "log.txt"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize all tables"""
    conn = get_connection()
    c = conn.cursor()

    # Identity table
    c.execute("""
        CREATE TABLE IF NOT EXISTS identity (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    # Conversations
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    # Knowledge base
    c.execute("""
        CREATE TABLE IF NOT EXISTS knowledge (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            content TEXT NOT NULL,
            source TEXT,
            embedding_hint TEXT,
            learned_at TEXT NOT NULL,
            usage_count INTEGER DEFAULT 0
        )
    """)

    # Knowledge tags for fast retrieval
    c.execute("""
        CREATE TABLE IF NOT EXISTS knowledge_tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            knowledge_id INTEGER,
            tag TEXT,
            FOREIGN KEY(knowledge_id) REFERENCES knowledge(id)
        )
    """)

    # Source code backups for rollback
    c.execute("""
        CREATE TABLE IF NOT EXISTS code_backups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL,
            files_json TEXT NOT NULL
        )
    """)

    # Operations log
    c.execute("""
        CREATE TABLE IF NOT EXISTS operations_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ─── Identity ────────────────────────────────────────────────────────────────

def set_identity(key: str, value: str):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO identity (key, value) VALUES (?, ?)", (key, value)
    )
    conn.commit()
    conn.close()


def get_identity(key: str, default=None):
    conn = get_connection()
    row = conn.execute("SELECT value FROM identity WHERE key=?", (key,)).fetchone()
    conn.close()
    return row["value"] if row else default


def is_first_run() -> bool:
    return get_identity("birth_date") is None


def initialize_identity(name: str, language: str = "en"):
    now = datetime.datetime.now().isoformat()
    set_identity("name", name)
    set_identity("birth_date", now)
    set_identity("language", language)
    set_identity("version", "1.0.0")


def get_age_string() -> str:
    birth_str = get_identity("birth_date")
    if not birth_str:
        return "newborn"
    birth = datetime.datetime.fromisoformat(birth_str)
    delta = datetime.datetime.now() - birth
    days = delta.days
    hours = delta.seconds // 3600
    minutes = (delta.seconds % 3600) // 60
    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


# ─── Conversations ────────────────────────────────────────────────────────────

def add_message(role: str, content: str):
    conn = get_connection()
    now = datetime.datetime.now().isoformat()
    conn.execute(
        "INSERT INTO conversations (role, content, timestamp) VALUES (?, ?, ?)",
        (role, content, now)
    )
    conn.commit()
    conn.close()


def get_recent_messages(limit: int = 20) -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT role, content, timestamp FROM conversations ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [{"role": r["role"], "content": r["content"], "timestamp": r["timestamp"]}
            for r in reversed(rows)]


def get_all_messages_for_api(limit: int = 30) -> list:
    """Returns messages in OpenAI API format"""
    msgs = get_recent_messages(limit)
    return [{"role": m["role"], "content": m["content"]} for m in msgs]


def clear_conversations():
    conn = get_connection()
    conn.execute("DELETE FROM conversations")
    conn.commit()
    conn.close()


# ─── Knowledge ───────────────────────────────────────────────────────────────

def save_knowledge(topic: str, content: str, source: str = "", tags: list = None):
    conn = get_connection()
    now = datetime.datetime.now().isoformat()
    # Avoid exact duplicates
    existing = conn.execute(
        "SELECT id FROM knowledge WHERE topic=? AND content=?", (topic, content)
    ).fetchone()
    if existing:
        conn.execute(
            "UPDATE knowledge SET usage_count=usage_count+1 WHERE id=?",
            (existing["id"],)
        )
        conn.commit()
        conn.close()
        return existing["id"]

    cur = conn.execute(
        "INSERT INTO knowledge (topic, content, source, embedding_hint, learned_at) VALUES (?, ?, ?, ?, ?)",
        (topic, content, source, topic.lower(), now)
    )
    kid = cur.lastrowid
    if tags:
        for tag in tags:
            conn.execute(
                "INSERT INTO knowledge_tags (knowledge_id, tag) VALUES (?, ?)",
                (kid, tag.lower())
            )
    conn.commit()
    conn.close()
    return kid


def search_knowledge(query: str, limit: int = 10) -> list:
    """Keyword-based search across knowledge base"""
    conn = get_connection()
    words = [w.strip().lower() for w in query.split() if len(w.strip()) > 2]
    if not words:
        conn.close()
        return []

    conditions = " OR ".join(["LOWER(k.topic) LIKE ? OR LOWER(k.content) LIKE ?" for _ in words])
    params = []
    for w in words:
        params.extend([f"%{w}%", f"%{w}%"])

    rows = conn.execute(
        f"""SELECT DISTINCT k.id, k.topic, k.content, k.source, k.learned_at, k.usage_count
            FROM knowledge k
            LEFT JOIN knowledge_tags kt ON k.id = kt.knowledge_id
            WHERE {conditions}
            ORDER BY k.usage_count DESC
            LIMIT ?""",
        params + [limit]
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_knowledge_count() -> int:
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) as cnt FROM knowledge").fetchone()
    conn.close()
    return row["cnt"]


def get_knowledge_size_kb() -> float:
    conn = get_connection()
    row = conn.execute("SELECT SUM(LENGTH(content)) as total FROM knowledge").fetchone()
    conn.close()
    total = row["total"] or 0
    return round(total / 1024, 1)


# ─── Code Backups ────────────────────────────────────────────────────────────

def save_code_backup(version: str, description: str, files: dict):
    conn = get_connection()
    now = datetime.datetime.now().isoformat()
    conn.execute(
        "INSERT INTO code_backups (version, description, created_at, files_json) VALUES (?, ?, ?, ?)",
        (version, description, now, json.dumps(files))
    )
    conn.commit()
    conn.close()


def get_latest_backup() -> dict | None:
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM code_backups ORDER BY id DESC LIMIT 1"
    ).fetchone()
    conn.close()
    if row:
        return {"version": row["version"], "description": row["description"],
                "created_at": row["created_at"], "files": json.loads(row["files_json"])}
    return None


def get_backup_count() -> int:
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) as cnt FROM code_backups").fetchone()
    conn.close()
    return row["cnt"]


# ─── Operations Log ──────────────────────────────────────────────────────────

def log_operation(level: str, message: str):
    """level: INFO | WARNING | ERROR | SUCCESS"""
    conn = get_connection()
    now = datetime.datetime.now().isoformat()
    conn.execute(
        "INSERT INTO operations_log (level, message, timestamp) VALUES (?, ?, ?)",
        (level, message, now)
    )
    conn.commit()
    conn.close()
    _write_log_file(level, message, now)
    _cleanup_old_logs()


def _write_log_file(level: str, message: str, timestamp: str):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")


def _cleanup_old_logs():
    """Keep only last 3 days of logs"""
    if not LOG_PATH.exists():
        return
    cutoff = datetime.datetime.now() - datetime.timedelta(days=3)
    lines_to_keep = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            try:
                ts_str = line.split("]")[0].strip("[")
                ts = datetime.datetime.fromisoformat(ts_str)
                if ts >= cutoff:
                    lines_to_keep.append(line)
            except Exception:
                lines_to_keep.append(line)
    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines_to_keep)

    # Also clean DB
    conn = get_connection()
    cutoff_str = cutoff.isoformat()
    conn.execute("DELETE FROM operations_log WHERE timestamp < ?", (cutoff_str,))
    conn.commit()
    conn.close()


def get_recent_operations(limit: int = 100) -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT level, message, timestamp FROM operations_log ORDER BY id DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in reversed(rows)]
