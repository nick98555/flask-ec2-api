import re
import sqlite3
import time
import os

LOG_PATH = "/var/log/auth.log"
DB_PATH = "syslogs.db"

FAILED_LOGIN_PATTERN = re.compile(
    r"Failed password for(?: invalid user)? (?P<user>\S+) from (?P<ip>\S+) port \d+ ssh2"
)

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS failed_logins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ip TEXT,
            user TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def parse_log():
    if not os.path.exists(LOG_PATH):
        print(f"Log file not found: {LOG_PATH}")
        return

    with open(LOG_PATH, "r") as f:
        lines = f.readlines()

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    for line in lines:
        match = FAILED_LOGIN_PATTERN.search(line)
        if match:
            user = match.group("user")
            ip = match.group("ip")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            c.execute(
                "INSERT INTO failed_logins (ip, user, timestamp) VALUES (?, ?, ?)",
                (ip, user, timestamp)
            )

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    parse_log()
    print("Log parsing complete. Failed login attempts stored in syslogs.db.")
