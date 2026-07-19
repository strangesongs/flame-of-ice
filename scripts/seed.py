#!/usr/bin/env python3
"""Initialize SQLite database and load show data."""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from db import DB_PATH, get_connection, init_db

DATA_PATH = ROOT / "data" / "shows.json"


def seed():
    if not DATA_PATH.exists():
        raise SystemExit(f"Missing {DATA_PATH}. Run: python scripts/generate_data.py")

    payload = json.loads(DATA_PATH.read_text())
    shows = payload["shows"]

    if DB_PATH.exists():
        DB_PATH.unlink()

    init_db()

    with get_connection() as conn:
        for show in shows:
            cur = conn.execute(
                """
                INSERT INTO shows (date, year, venue, place, notes, source)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    show["date"],
                    show["year"],
                    show["venue"],
                    show["place"],
                    show.get("notes"),
                    show.get("source"),
                ),
            )
            show_id = cur.lastrowid
            for rec in show.get("recordings", []):
                conn.execute(
                    """
                    INSERT INTO recordings (show_id, url, source, title)
                    VALUES (?, ?, ?, ?)
                    """,
                    (show_id, rec["url"], rec["source"], rec.get("title")),
                )

        conn.commit()
        count_shows = conn.execute("SELECT COUNT(*) FROM shows").fetchone()[0]
        count_recs = conn.execute("SELECT COUNT(*) FROM recordings").fetchone()[0]

    print(f"Seeded {count_shows} shows, {count_recs} recording links → {DB_PATH}")


if __name__ == "__main__":
    seed()
