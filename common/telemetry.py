import sqlite3, time, json, os
from typing import Optional, Dict


DB_PATH = os.getenv("TELEMETRY_DB", "telemetry.db")


def _ensure():
with sqlite3.connect(DB_PATH) as con:
con.execute(
"""
CREATE TABLE IF NOT EXISTS events (
ts REAL,
project TEXT,
kind TEXT,
meta TEXT
)
"""
)


def log_event(project: str, kind: str, meta: Optional[Dict] = None):
_ensure()
with sqlite3.connect(DB_PATH) as con:
con.execute(
"INSERT INTO events (ts, project, kind, meta) VALUES (?, ?, ?, ?)",
(time.time(), project, kind, json.dumps(meta or {}))
)
