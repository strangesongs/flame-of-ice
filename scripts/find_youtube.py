#!/usr/bin/env python3
"""
Search YouTube for Les Rallizes Dénudés live uploads.

Requires yt-dlp: pip install yt-dlp

Usage:
  python scripts/find_youtube.py
  python scripts/find_youtube.py "1980 Yaneura"
"""

import json
import subprocess
import sys


DEFAULT_QUERIES = [
    "Les Rallizes Denudes live full",
    "Les Rallizes Denudes 1977 live",
    "Les Rallizes Denudes 1980 Yaneura live",
    "Les Rallizes Denudes 1993 Citta live",
    "Les Rallizes Denudes OZ Tapes live",
    "Les Rallizes Denudes Jittoku live",
    "裸のラリーズ ライブ",
]


def search(query: str, limit: int = 15) -> list[dict]:
    cmd = ["yt-dlp", f"ytsearch{limit}:{query}", "--flat-playlist", "-j"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    results = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        title = d.get("title", "")
        if "rallizes" not in title.lower() and "ラリーズ" not in title:
            continue
        vid = d.get("id")
        if not vid:
            continue
        results.append(
            {
                "id": vid,
                "title": title,
                "url": f"https://www.youtube.com/watch?v={vid}",
            }
        )
    return results


def main():
    queries = sys.argv[1:] if len(sys.argv) > 1 else DEFAULT_QUERIES
    seen = set()
    all_results = []

    for q in queries:
        for item in search(q):
            if item["id"] in seen:
                continue
            seen.add(item["id"])
            all_results.append(item)

    print(f"Found {len(all_results)} videos\n")
    for item in sorted(all_results, key=lambda x: x["title"].lower()):
        print(item["url"])
        print(f"  {item['title']}")
        print()


if __name__ == "__main__":
    main()
