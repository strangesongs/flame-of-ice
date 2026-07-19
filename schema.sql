-- Flame of Ice: Les Rallizes Dénudés live show archive

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS shows (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,           -- ISO 8601 (YYYY-MM-DD)
    year INTEGER NOT NULL,
    venue TEXT NOT NULL,
    place TEXT NOT NULL,          -- city/region and country, e.g. "Tokyo, Japan"
    notes TEXT,
    source TEXT,                  -- internal provenance (not shown on site)
    UNIQUE (date, venue, place)
);

CREATE TABLE IF NOT EXISTS recordings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    show_id INTEGER NOT NULL REFERENCES shows(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    source TEXT NOT NULL,         -- e.g. Discogs, YouTube, bootleg.fm
    title TEXT
);

CREATE INDEX IF NOT EXISTS idx_shows_date ON shows(date);
CREATE INDEX IF NOT EXISTS idx_shows_year ON shows(year);
CREATE INDEX IF NOT EXISTS idx_recordings_show_id ON recordings(show_id);
