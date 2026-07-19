import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "flame_of_ice.db"
SCHEMA_PATH = ROOT / "schema.sql"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    schema = SCHEMA_PATH.read_text()
    with get_connection() as conn:
        conn.executescript(schema)
        conn.commit()
