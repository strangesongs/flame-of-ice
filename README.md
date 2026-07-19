# Flame of Ice

An archive of known live performances by **Les Rallizes Dénudés** (裸のラリーズ).

SQLite database + minimal Flask API + plain HTML frontend.

## Setup

```bash
cd flame-of-ice
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python scripts/generate_data.py   # build data/shows.json from sources
python scripts/seed.py            # create flame_of_ice.db

python app.py                     # http://127.0.0.1:5050 (Flask API for local dev)
```

## Deploy

The live site is static and hosted on GitHub Pages at:

**https://strangesongs.github.io/flame-of-ice/**

Pushes to `main` run `.github/workflows/deploy.yml`, which rebuilds `shows.json` and publishes `public/`.

To update the live site after editing show data:

```bash
python scripts/generate_data.py
git add data/shows.json public/data/shows.json
git commit -m "Update show data"
git push
```

## Database

Schema lives in `schema.sql`. Two tables:

- **shows** — date, year, venue, place, notes, source (source is internal only)
- **recordings** — multiple external links per show (Discogs, bootleg.fm, official site)

Example queries:

```bash
sqlite3 flame_of_ice.db

SELECT date, venue, place FROM shows ORDER BY date DESC LIMIT 10;

SELECT s.date, s.venue, s.place, r.title, r.url
FROM shows s
JOIN recordings r ON r.show_id = s.id
WHERE s.year = 1980;
```

## Data sources

Primary show index: [setlist.fm](https://www.setlist.fm/setlists/les-rallizes-denudes-3bd6ac04.html) (114 concerts).

Supplemental entries and recording links from bootleg.fm, Discogs, Temporal Drift official reissues, the Live Archive (1973–1993) compilation index, and matched YouTube uploads.

To search for more YouTube links:

```bash
pip install yt-dlp
python scripts/find_youtube.py
python scripts/find_youtube.py "1983 Hosei live"
```

Add matches to `YOUTUBE_RECORDINGS` in `scripts/generate_data.py`, then re-seed.

Many shows have no known recording.

## Adding shows

1. Edit `scripts/generate_data.py` (add to `SETLIST_FM`, `SUPPLEMENTAL`, or `RECORDINGS`)
2. Re-run `generate_data.py` and `seed.py`

Or insert directly via SQL:

```sql
INSERT INTO shows (date, year, venue, place, source)
VALUES ('1980-01-01', 1980, 'Yaneura', 'Tokyo, Japan', 'manual');

INSERT INTO recordings (show_id, url, source, title)
VALUES (last_insert_rowid(), 'https://www.discogs.com/...', 'Discogs', 'Release title');
```
