import sqlite3
from .config import DB_PATH

def init():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("CREATE TABLE IF NOT EXISTS videos(video_id TEXT PRIMARY KEY, title TEXT, status TEXT, ts DATETIME DEFAULT CURRENT_TIMESTAMP)")

def seen(video_id):
    init()
    with sqlite3.connect(DB_PATH) as c:
        return c.execute("SELECT 1 FROM videos WHERE video_id=?", (video_id,)).fetchone() is not None

def mark(video_id, title, status):
    init()
    with sqlite3.connect(DB_PATH) as c:
        c.execute("INSERT OR REPLACE INTO videos(video_id,title,status) VALUES(?,?,?)", (video_id, title, status))

def all_videos():
    init()
    with sqlite3.connect(DB_PATH) as c:
        return [{"video_id": r[0], "title": r[1], "status": r[2]} for r in c.execute("SELECT video_id,title,status FROM videos ORDER BY ts DESC LIMIT 50")]
