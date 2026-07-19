from pathlib import Path

from flask import Flask, jsonify, send_from_directory

from db import get_connection, init_db

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"

app = Flask(__name__, static_folder=str(PUBLIC), static_url_path="")


@app.route("/api/shows")
def list_shows():
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT s.id, s.date, s.year, s.venue, s.place, s.notes
            FROM shows s
            ORDER BY s.date ASC, s.venue ASC, s.place ASC
            """
        ).fetchall()

        shows = []
        for row in rows:
            recordings = conn.execute(
                """
                SELECT url, source, title
                FROM recordings
                WHERE show_id = ?
                ORDER BY source ASC, title ASC
                """,
                (row["id"],),
            ).fetchall()
            shows.append(
                {
                    "id": row["id"],
                    "date": row["date"],
                    "year": row["year"],
                    "venue": row["venue"],
                    "place": row["place"],
                    "notes": row["notes"],
                    "recordings": [dict(r) for r in recordings],
                }
            )

    return jsonify({"shows": shows, "count": len(shows)})


@app.route("/")
def index():
    return send_from_directory(PUBLIC, "index.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5050)
