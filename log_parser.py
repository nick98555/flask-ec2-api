import sqlite3
import time
import subprocess

DB_PATH = "syslogs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS uptime_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            uptime TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_uptime():
    result = subprocess.run(["uptime", "-p"], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def log_uptime():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    uptime = get_uptime()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "INSERT INTO uptime_log (timestamp, uptime) VALUES (?, ?_
