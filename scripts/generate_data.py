#!/usr/bin/env python3
"""Build data/shows.json from compiled research sources."""

import json
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "shows.json"
PUBLIC_OUT = ROOT / "public" / "data" / "shows.json"

MONTHS = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}


def parse_date(display: str) -> tuple[str, int]:
    """Convert 'Oct 4 1996' to ('1996-10-04', 1996)."""
    parts = display.split()
    month = MONTHS[parts[0]]
    day = int(parts[1])
    year = int(parts[2])
    return f"{year:04d}-{month:02d}-{day:02d}", year


def split_location(location: str) -> tuple[str, str]:
    """Split 'Yaneura, Tokyo, Japan' into venue and place."""
    location = location.strip()
    if location.endswith(", Japan"):
        body = location[: -len(", Japan")]
        idx = body.rfind(", ")
        if idx == -1:
            return body, "Japan"
        venue = body[:idx]
        city = body[idx + 2 :]
        return venue, f"{city}, Japan"
    return location, ""


def show_from_location(date: str, year: int, location: str, **extra) -> dict:
    venue, place = split_location(location)
    return {
        "date": date,
        "year": year,
        "venue": venue,
        "place": place,
        "notes": extra.get("notes"),
        "source": extra.get("source"),
        "recordings": [],
    }


# 114 concerts from setlist.fm (primary index) + supplemental documented shows
SETLIST_FM = [
    ("Oct 4 1996", "CLUB CITTA', Kawasaki, Japan"),
    ("Feb 24 1995", "CLUB CITTA', Kawasaki, Japan"),
    ("Sep 9 1994", "CLUB CITTA', Kawasaki, Japan"),
    ("Jul 10 1994", "Kyoto Daigaku, Seibu Koudou, Kyoto, Japan"),
    ("Feb 17 1993", "CLUB CITTA', Kawasaki, Japan"),
    ("Feb 13 1993", "Kichijouji Baus Theater, Musashino, Japan"),
    ("Jul 28 1988", "CROCODILE, Tokyo, Japan"),
    ("Jun 9 1988", "Rock-May-Kan, Tokyo, Japan"),
    ("Apr 18 1988", "Rock-May-Kan, Tokyo, Japan"),
    ("Mar 23 1988", "CROCODILE, Tokyo, Japan"),
    ("Feb 23 1988", "Rock-May-Kan, Tokyo, Japan"),
    ("Jan 18 1988", "Rock-May-Kan, Tokyo, Japan"),
    ("Dec 9 1987", "CROCODILE, Tokyo, Japan"),
    ("Nov 1 1987", "Waseda Daigaku, Kinenkaidou, Tokyo, Japan"),
    ("Sep 2 1987", "Rock-May-Kan, Tokyo, Japan"),
    ("Aug 14 1987", "Rock-May-Kan, Tokyo, Japan"),
    ("Jun 23 1987", "CROCODILE, Tokyo, Japan"),
    ("May 13 1987", "Rock-May-Kan, Tokyo, Japan"),
    ("Apr 8 1987", "Rock-May-Kan, Tokyo, Japan"),
    ("Jan 22 1987", "Rock-May-Kan, Tokyo, Japan"),
    ("Oct 1 1986", "CROCODILE, Tokyo, Japan"),
    ("Sep 9 1986", "Rock-May-Kan, Tokyo, Japan"),
    ("Jul 9 1986", "CROCODILE, Tokyo, Japan"),
    ("May 21 1986", "Yaneura, Tokyo, Japan"),
    ("Apr 11 1986", "Rock-May-Kan, Tokyo, Japan"),
    ("Dec 18 1985", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Oct 1 1985", "Rock-May-Kan, Tokyo, Japan"),
    ("Aug 22 1985", "Yaneura, Tokyo, Japan"),
    ("Apr 30 1985", "Rock-May-Kan, Tokyo, Japan"),
    ("Apr 4 1985", "Yaneura, Tokyo, Japan"),
    ("Jan 29 1985", "Rock-May-Kan, Tokyo, Japan"),
    ("Dec 22 1984", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Oct 17 1984", "Rock-May-Kan, Tokyo, Japan"),
    ("Aug 13 1984", "Rock-May-Kan, Tokyo, Japan"),
    ("Dec 24 1983", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Nov 10 1983", "Yokohama Kokuritsu Daigaku, Yokohama, Japan"),
    ("Oct 10 1983", "Rock-May-Kan, Tokyo, Japan"),
    ("Aug 11 1983", "Chicken Shack, Fussa, Japan"),
    ("Aug 8 1983", "Shimokitazawa Odeon-za, Tokyo, Japan"),
    ("May 7 1983", "Kyoto Daigaku, Seibu Koudou, Kyoto, Japan"),
    ("Apr 20 1983", "Rock-May-Kan, Tokyo, Japan"),
    ("Mar 29 1983", "Yaneura, Tokyo, Japan"),
    ("Feb 18 1983", "Yaneura, Tokyo, Japan"),
    ("Dec 18 1982", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Oct 2 1982", "Keiou Gijuku Daigaku, Hiyoshi Campus, Yokohama, Japan"),
    ("Oct 1 1982", "Rock-May-Kan, Tokyo, Japan"),
    ("Dec 19 1981", "Yaneura, Tokyo, Japan"),
    ("Nov 6 1981", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Aug 23 1981", "Yaneura, Tokyo, Japan"),
    ("Aug 18 1981", "Yaneura, Tokyo, Japan"),
    ("Mar 23 1981", "Yaneura, Tokyo, Japan"),
    ("Dec 13 1980", "Yaneura, Tokyo, Japan"),
    ("Nov 24 1980", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Nov 7 1980", "Kanagawa Daigaku, Yokohama Campus, Yokohama, Japan"),
    ("Oct 29 1980", "Yaneura, Tokyo, Japan"),
    ("Sep 11 1980", "Yaneura, Tokyo, Japan"),
    ("Sep 9 1980", "Mars Studio, Kunitachi, Japan"),
    ("Sep 6 1980", "Mars Studio, Kunitachi, Japan"),
    ("Sep 4 1980", "Mars Studio, Kunitachi, Japan"),
    ("Aug 14 1980", "Yaneura, Tokyo, Japan"),
    ("Jan 16 1980", "Yaneura, Tokyo, Japan"),
    ("Dec 4 1979", "Yaneura, Tokyo, Japan"),
    ("Oct 27 1979", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Jun 13 1979", "Yaneura, Tokyo, Japan"),
    ("Apr 25 1979", "Yaneura, Tokyo, Japan"),
    ("Mar 7 1979", "Chicken Shack, Fussa, Japan"),
    ("Feb 18 1979", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Nov 1 1978", "Aoyama Bell Commons, Tokyo, Japan"),
    ("Aug 12 1978", "Shishiku Kougen Ski-jou, Tsurugi, Japan"),
    ("Aug 25 1977", "Kawaguchiko, Kawaguchiko, Japan"),
    ("Aug 21 1977", "Fuji Yagai Ongakudo, Narusawa, Japan"),
    ("Aug 13 1977", "Shishiku Kougen Ski-jou, Tsurugi, Japan"),
    ("Jul 22 1977", "Nichifutsu Kaikan, Tokyo, Japan"),
    ("Jun 25 1977", "Koumyou Biru, Hachiouji, Japan"),
    ("Mar 12 1977", "Tachikawa Shakai Kyouiku Kaikan, Tachikawa, Japan"),
    ("Dec 17 1976", "Tachikawa Shakai Kyouiku Kaikan, Tachikawa, Japan"),
    ("Nov 15 1976", "Yaneura, Tokyo, Japan"),
    ("Oct 30 1976", "Kinjou Gakuin Daigaku, Shinsei Koudou, Nagoya, Japan"),
    ("Sep 22 1976", "Yaneura, Tokyo, Japan"),
    ("Aug 11 1976", "Yaneura, Tokyo, Japan"),
    ("Aug 3 1976", "Shishiku Kougen Ski-jou, Tsurugi, Japan"),
    ("Jul 30 1976", "Jittoku, Kyoto, Japan"),
    ("Jul 25 1976", "Yaneura, Tokyo, Japan"),
    ("Jun 22 1976", "Yaneura, Tokyo, Japan"),
    ("May 25 1976", "Yaneura, Tokyo, Japan"),
    ("May 16 1976", "Yaneura, Tokyo, Japan"),
    ("Apr 12 1976", "Yaneura, Tokyo, Japan"),
    ("Feb 15 1976", "Yaneura, Tokyo, Japan"),
    ("Jan 17 1976", "Housei Daigaku, Gakusei Kaikan, Tokyo, Japan"),
    ("Nov 3 1975", "Meiji Gakuin Daigaku, Shirokane Campus, Tokyo, Japan"),
    ("Oct 5 1975", "Kyoto Daigaku, Seibu Koudou, Kyoto, Japan"),
    ("Oct 1 1975", "CLUB ADAN, Tokyo, Japan"),
    ("Aug 23 1975", "Mizunashiyama Ski-jou, Kaga, Japan"),
    ("Jun 28 1975", "Kanagawa Daigaku, Yokohama Campus, Yokohama, Japan"),
    ("May 25 1975", "Yaneura, Tokyo, Japan"),
    ("Apr 20 1975", "Nippon Zan Myoho Ji, Gotenba, Japan"),
    ("Nov 2 1974", "Tama Bijutsu Daigaku, Hachiouji Campus, Taiikukan, Hachiouji, Japan"),
    ("Jul 13 1974", "Meiji Gakuin Daigaku, Shirokane Campus, Tokyo, Japan"),
    ("Jan 26 1974", "Sugino Koudou, Tokyo, Japan"),
    ("Jan 1 1974", "Nippon Zan Myoho Ji, Gotenba, Japan"),
    ("Nov 3 1973", "Saitama Daigaku, Taiikukan, Urawa, Japan"),
    ("Nov 1 1973", "Meiji Gakuin Daigaku, Shirokane Campus, Tokyo, Japan"),
    ("Sep 2 1973", "OZ, Musashino, Japan"),
    ("Aug 25 1973", "Rimpoen, Kaga, Japan"),
    ("Jan 1 1973", "Meiji Gakuin Daigaku, Shirokane Campus, Tokyo, Japan"),
    ("Dec 29 1972", "OZ, Musashino, Japan"),
    ("Oct 14 1972", "OZ, Musashino, Japan"),
    ("Aug 16 1972", "Kyoto Daigaku, Seibu Koudou, Kyoto, Japan"),
    ("Jul 26 1970", "Fuji-Q Highland, Fuji-Yoshida, Japan"),
    ("May 1 1970", "Doushisha Daigaku, Kyoto, Japan"),
    ("Oct 18 1969", "Kyoto Kyouiku Bunka Center, Kyoto, Japan"),
    ("Apr 26 1969", "Gallery Iteza, Kyoto, Japan"),
    ("Apr 12 1969", "Kyoto Daigaku, A-goukan Chika, Kyoto, Japan"),
    ("Nov 29 1968", "Doushisha Daigaku, Kyoto, Japan"),
]

# Additional documented performances not indexed on setlist.fm
SUPPLEMENTAL = [
    {
        "date": "1993-12-24",
        "year": 1993,
        "location": "Mushroom, Tokyo, Japan",
        "notes": "Side project performance (Niplets + Mizutani); documented in Live Archive (1973–1993).",
        "source": "Album of the Year / Live Archive",
    },
    {
        "date": "1987-09-21",
        "year": 1987,
        "location": "Rock-May-Kan (Rokumeikan), Tokyo, Japan",
        "notes": "Documented in Live Archive; may overlap with indexed Rokumeikan dates.",
        "source": "Album of the Year / Live Archive",
    },
    {
        "date": "1980-11-08",
        "year": 1980,
        "location": "Kanagawa Daigaku, Yokohama Campus, Yokohama, Japan",
        "notes": "Second night of two-day engagement (Nov 7–8, 1980).",
        "source": "Lineapp / fan documentation",
    },
    {
        "date": "1975-10-01",
        "year": 1975,
        "location": "Adan Music Studio, Tokyo, Japan",
        "notes": "Studio session; often grouped with live archive material.",
        "source": "Album of the Year / Live Archive",
    },
    {
        "date": "1973-03-04",
        "year": 1973,
        "location": "Musashino Public Hall, Tokyo, Japan",
        "notes": "Referenced on official Les Rallizes Dénudés site.",
        "source": "lesrallizesdenudes-official.com",
    },
]

# Recording links keyed by (date, location substring match)
RECORDINGS = [
    {
        "match_date": "1996-10-04",
        "match_location": "CITTA",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1993-02-17",
        "match_location": "CITTA",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
            {"url": "https://www.discogs.com/master/2849784-Les-Rallizes-D%C3%A9nud%C3%A9s-Citta-93", "source": "Discogs", "title": "CITTA' '93 (Temporal Drift, 2023)"},
            {"url": "https://lesrallizesdenudes-official.com/", "source": "official", "title": "CITTA' '93 — official release"},
        ],
    },
    {
        "match_date": "1993-02-13",
        "match_location": "Baus",
        "recordings": [
            {"url": "https://www.discogs.com/master/2849783-Les-Rallizes-D%C3%A9nud%C3%A9s-Baus-93", "source": "Discogs", "title": "BAUS '93 (Temporal Drift, 2023)"},
            {"url": "https://lesrallizesdenudes-official.com/", "source": "official", "title": "BAUS '93 — official release"},
        ],
    },
    {
        "match_date": "1986-05-21",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1985-12-18",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1984-10-17",
        "match_location": "Rock-May-Kan",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1983-05-07",
        "match_location": "Kyoto Daigaku",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1982-10-02",
        "match_location": "Keiou",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1981-12-19",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1981-11-06",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1981-03-23",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1980-12-13",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.discogs.com/master/338539-Les-Rallizes-D%C3%A9nud%C3%A9s-Decembers-Black-Children-Live-13121980", "source": "Discogs", "title": "December's Black Children (1989 bootleg)"},
            {"url": "https://lrd.bootleg.fm/", "source": "bootleg.fm", "title": "Bootleg archive entry"},
        ],
    },
    {
        "match_date": "1980-09-09",
        "match_location": "Mars Studio",
        "recordings": [
            {"url": "https://www.discogs.com/master/338537-Les-Rallizes-D%C3%A9nud%C3%A9s-Mars-Studio-1980", "source": "Discogs", "title": "Mars Studio 1980"},
        ],
    },
    {
        "match_date": "1980-09-06",
        "match_location": "Mars Studio",
        "recordings": [
            {"url": "https://www.discogs.com/master/338537-Les-Rallizes-D%C3%A9nud%C3%A9s-Mars-Studio-1980", "source": "Discogs", "title": "Mars Studio 1980"},
        ],
    },
    {
        "match_date": "1980-09-04",
        "match_location": "Mars Studio",
        "recordings": [
            {"url": "https://www.discogs.com/master/338537-Les-Rallizes-D%C3%A9nud%C3%A9s-Mars-Studio-1980", "source": "Discogs", "title": "Mars Studio 1980"},
        ],
    },
    {
        "match_date": "1980-10-29",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.discogs.com/master/338543-Les-Rallizes-D%C3%A9nud%C3%A9s-YaneUra-Oct-80", "source": "Discogs", "title": "YaneUra Oct. '80 (Temporal Drift, 2024)"},
        ],
    },
    {
        "match_date": "1980-09-11",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.discogs.com/master/338544-Les-Rallizes-D%C3%A9nud%C3%A9s-YaneUra-Sept-80", "source": "Discogs", "title": "YaneUra Sept. '80 (Temporal Drift, 2024)"},
        ],
    },
    {
        "match_date": "1981-08-23",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.discogs.com/master/338538-Les-Rallizes-D%C3%A9nud%C3%A9s-Great-White-Wonder", "source": "Discogs", "title": "Great White Wonder (2006 bootleg)"},
        ],
    },
    {
        "match_date": "1983-12-24",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://www.discogs.com/search/?q=shrieking+eve+night+rallizes", "source": "Discogs", "title": "Shrieking Eve Night: Live at Hosei University, 12/24/83"},
        ],
    },
    {
        "match_date": "1977-03-12",
        "match_location": "Tachikawa",
        "recordings": [
            {"url": "https://www.discogs.com/master/338535-Les-Rallizes-D%C3%A9nud%C3%A9s-77-Live", "source": "Discogs", "title": "'77 Live (Rivista/Temporal Drift, 1991)"},
            {"url": "https://lesrallizesdenudes-official.com/", "source": "official", "title": "'77 Live — official reissue"},
        ],
    },
    {
        "match_date": "1977-07-22",
        "match_location": "Nichifutsu",
        "recordings": [
            {"url": "https://www.discogs.com/master/338535-Les-Rallizes-D%C3%A9nud%C3%A9s-77-Live", "source": "Discogs", "title": "'77 Live (Rivista/Temporal Drift, 1991)"},
            {"url": "https://lesrallizesdenudes-official.com/", "source": "official", "title": "'77 Live — official reissue"},
        ],
    },
    {
        "match_date": "1976-12-17",
        "match_location": "Tachikawa",
        "recordings": [
            {"url": "https://www.discogs.com/master/338542-Les-Rallizes-D%C3%A9nud%C3%A9s-Jittoku-76", "source": "Discogs", "title": "Jittoku '76 (Temporal Drift, 2025)"},
        ],
    },
    {
        "match_date": "1976-07-30",
        "match_location": "Jittoku",
        "recordings": [
            {"url": "https://www.discogs.com/master/338542-Les-Rallizes-D%C3%A9nud%C3%A9s-Jittoku-76", "source": "Discogs", "title": "Jittoku '76 (Temporal Drift, 2025)"},
        ],
    },
    {
        "match_date": "1974-07-13",
        "match_location": "Meiji Gakuin",
        "recordings": [
            {"url": "https://www.discogs.com/master/338536-Les-Rallizes-D%C3%A9nud%C3%A9s-Electric-Pure-Land", "source": "Discogs", "title": "Electric Pure Land (2014 bootleg; recorded 1974)"},
        ],
    },
    {
        "match_date": "1973-09-02",
        "match_location": "OZ",
        "recordings": [
            {"url": "https://www.discogs.com/master/338534-Les-Rallizes-D%C3%A9nud%C3%A9s-The-OZ-Tapes", "source": "Discogs", "title": "The OZ Tapes (Temporal Drift, 2022)"},
            {"url": "https://lesrallizesdenudes-official.com/", "source": "official", "title": "The OZ Tapes — official release"},
        ],
    },
    {
        "match_date": "1980-12-13",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.discogs.com/master/338541-Les-Rallizes-D%C3%A9nud%C3%A9s-Double-Heads-Legendary-Live-Yaneura-Shibuya-Tokyo-1980-1981", "source": "Discogs", "title": "Double Heads: Legendary Live (1980–1981)"},
        ],
    },
    {
        "match_date": "1981-12-19",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.discogs.com/master/338541-Les-Rallizes-D%C3%A9nud%C3%A9s-Double-Heads-Legendary-Live-Yaneura-Shibuya-Tokyo-1980-1981", "source": "Discogs", "title": "Double Heads: Legendary Live (1980–1981)"},
        ],
    },
]

# YouTube uploads matched to specific dates/venues (fan uploads, remasters, official rips)
YOUTUBE_RECORDINGS = [
    {
        "match_date": "1973-09-02",
        "match_location": "OZ",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=zEVZnF0wYsE", "source": "YouTube", "title": "Oz Days Live — Session 1 (1973)"},
            {"url": "https://www.youtube.com/watch?v=3R7l8Stv8go", "source": "YouTube", "title": "1973 Live"},
        ],
    },
    {
        "match_date": "1973-11-03",
        "match_location": "Saitama",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=LPLMMJKEEak", "source": "YouTube", "title": "Electric Allnight Concert, 11/3–4/73 (Remastered 2022)"},
        ],
    },
    {
        "match_date": "1974-07-13",
        "match_location": "Meiji Gakuin",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=8spvjza-jW4", "source": "YouTube", "title": "Live at Meiji Gakuin University 13.7.1974 (Alternate Soundboard)"},
        ],
    },
    {
        "match_date": "1975-06-28",
        "match_location": "Kanagawa",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=SQZEOH_OSSo", "source": "YouTube", "title": "Allnight Rainbow Show (1975)"},
        ],
    },
    {
        "match_date": "1975-10-01",
        "match_location": "Adan",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=4f_cTzNpaUE", "source": "YouTube", "title": "1975/10/01 — Full Performance"},
        ],
    },
    {
        "match_date": "1976-07-30",
        "match_location": "Jittoku",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=aqucRzGd340", "source": "YouTube", "title": "Live at Jittoku (1976)"},
            {"url": "https://www.youtube.com/watch?v=e61otxDhyJI", "source": "YouTube", "title": "1976 Kyoto (remastered)"},
        ],
    },
    {
        "match_date": "1976-08-03",
        "match_location": "Shishiku",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=BYteF-C4S_o", "source": "YouTube", "title": "3rd Sunset Festival — August 3, 1976 (Full Version)"},
            {"url": "https://www.youtube.com/watch?v=swSVFrli43Y", "source": "YouTube", "title": "Yuyake Matsuri 1976 — setlist restored"},
        ],
    },
    {
        "match_date": "1976-10-30",
        "match_location": "Kinjou",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=AbnVSKntfX0", "source": "YouTube", "title": "Live at Kinjo Gakuin University (1976)"},
        ],
    },
    {
        "match_date": "1977-03-12",
        "match_location": "Tachikawa",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=xoYVEQeJ4WQ", "source": "YouTube", "title": "'77 Live (full album)"},
            {"url": "https://www.youtube.com/watch?v=xknETt07xJo", "source": "YouTube", "title": "Live at Tachikawa Social Education Center (1977)"},
            {"url": "https://www.youtube.com/watch?v=svqFV9oewrs", "source": "YouTube", "title": "'77 Live"},
        ],
    },
    {
        "match_date": "1977-08-13",
        "match_location": "Shishiku",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=gO-Q_n4YKVQ", "source": "YouTube", "title": "4th Sunset Carnival, 8/13–14/77 (Remastered 2022)"},
        ],
    },
    {
        "match_date": "1978-11-01",
        "match_location": "Aoyama",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=pTRkRRrO_1c", "source": "YouTube", "title": "Live at Aoyama Bell Commons (1978)"},
        ],
    },
    {
        "match_date": "1980-08-14",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=5ZFQG-2v-w0", "source": "YouTube", "title": "LIVE 14 Aug. 1980 at Yaneura, Shibuya (with Fujio Yamaguchi)"},
            {"url": "https://www.youtube.com/watch?v=fW5zN5tI7bk", "source": "YouTube", "title": "The Last One (Double Heads — 14 August 1980)"},
        ],
    },
    {
        "match_date": "1980-09-09",
        "match_location": "Mars Studio",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=IzvwP5XuWH0", "source": "YouTube", "title": "Mars Studio 1980"},
            {"url": "https://www.youtube.com/watch?v=2aUwYPA0kss", "source": "YouTube", "title": "Enter the Mirror 2 (Mars Studio)"},
        ],
    },
    {
        "match_date": "1980-10-29",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=kvq9Glx9H1A", "source": "YouTube", "title": "LIVE 1980-10-29, Yaneura Shibuya (original audience tapes)"},
            {"url": "https://www.youtube.com/watch?v=KsDV770eZoE", "source": "YouTube", "title": "LIVE 29 Oct. 1980 at Yaneura, Shibuya (with Fujio Yamaguchi)"},
        ],
    },
    {
        "match_date": "1980-11-24",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=cliXAyEgpJ8", "source": "YouTube", "title": "Live at Hosei University, November 24, 1980"},
            {"url": "https://www.youtube.com/watch?v=wQ4cu1yMLp0", "source": "YouTube", "title": "LIVE Nov. 24, 1980 at Hosei Daigaku (with Fujio Yamaguchi)"},
        ],
    },
    {
        "match_date": "1980-12-13",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=3T7jjTalmio", "source": "YouTube", "title": "Deeper Than The Night — 13 Dec 1980"},
            {"url": "https://www.youtube.com/watch?v=Gg52D3CCpgQ", "source": "YouTube", "title": "The Last One (December's Black Children)"},
            {"url": "https://www.youtube.com/watch?v=EWQjXEVDcpg", "source": "YouTube", "title": "Double Heads: Legendary Live (1980–1981) — full album"},
        ],
    },
    {
        "match_date": "1981-11-06",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=yUcG7psg5kM", "source": "YouTube", "title": "Live at Hosei University, 11/6/81 (Remastered 2022)"},
        ],
    },
    {
        "match_date": "1981-12-19",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=EWQjXEVDcpg", "source": "YouTube", "title": "Double Heads: Legendary Live (1980–1981) — full album"},
        ],
    },
    {
        "match_date": "1982-10-02",
        "match_location": "Keiou",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=4TgfQzfOmvA", "source": "YouTube", "title": "Keio Gijuku University 1982"},
            {"url": "https://www.youtube.com/watch?v=N_rgvJRh5jU", "source": "YouTube", "title": "Dream Divides Grass (October 1982 at Keio University)"},
        ],
    },
    {
        "match_date": "1982-12-18",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=c6CrBhawRMY", "source": "YouTube", "title": "LIVE 1982-12-18, Hosei University (alternate sources)"},
            {"url": "https://www.youtube.com/watch?v=0_duspI5Xzo", "source": "YouTube", "title": "LIVE 1982-12-18, Hosei University (remastered video)"},
        ],
    },
    {
        "match_date": "1983-03-29",
        "match_location": "Yaneura",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=ru5DLr-0e74", "source": "YouTube", "title": "LIVE 1983-03-29, Yaneura, Shibuya"},
        ],
    },
    {
        "match_date": "1983-05-07",
        "match_location": "Kyoto Daigaku",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=e5KqJ3X3Geg", "source": "YouTube", "title": "1983 Kyoto (remastered and pitch corrected)"},
        ],
    },
    {
        "match_date": "1983-11-10",
        "match_location": "Yokohama",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=QW-b8Adc4Gc", "source": "YouTube", "title": "LIVE 1983-11-10, Yokohama National University (remastered)"},
        ],
    },
    {
        "match_date": "1983-12-24",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=VTikB3xlvCs", "source": "YouTube", "title": "Shrieking Eve Night: 12/24/83 (Remastered, 2024)"},
            {"url": "https://www.youtube.com/watch?v=gaCoZ_K3EZw", "source": "YouTube", "title": "Enter The Mirror (12/24/1983)"},
        ],
    },
    {
        "match_date": "1984-08-13",
        "match_location": "Rock-May-Kan",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=GgNTmFPnaEU", "source": "YouTube", "title": "Live at Meguro Rokumeikan, 13.8.1984 (remastered)"},
        ],
    },
    {
        "match_date": "1985-04-30",
        "match_location": "Rock-May-Kan",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=pUjVee9VRpI", "source": "YouTube", "title": "1985-04-30 Live at Meguro Rokumeikan"},
        ],
    },
    {
        "match_date": "1985-12-18",
        "match_location": "Housei",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=NTgOF--U-Sw", "source": "YouTube", "title": "Hosei Daigaku 18 Dec '85"},
        ],
    },
    {
        "match_date": "1987-08-14",
        "match_location": "Rock-May-Kan",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=tmS6LiPkrAo", "source": "YouTube", "title": "LIVE 14 Aug. 1987 at Meguro Rokumeikan"},
        ],
    },
    {
        "match_date": "1988-07-28",
        "match_location": "CROCODILE",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=VY5fiJXVjkw", "source": "YouTube", "title": "1988 Shibuya (remastered)"},
        ],
    },
    {
        "match_date": "1993-02-13",
        "match_location": "Baus",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=UxEkZzrmZgY", "source": "YouTube", "title": "1993/02/13 — Full Performance"},
            {"url": "https://www.youtube.com/watch?v=ZYh97yvulAo", "source": "YouTube", "title": "Kichijouji Baus Theater (Feb 13 1993)"},
        ],
    },
    {
        "match_date": "1993-02-17",
        "match_location": "CITTA",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=tJuhl2ejIxo", "source": "YouTube", "title": "LIVE 1993-02-17, CLUB CITTA' (remastered)"},
            {"url": "https://www.youtube.com/watch?v=ENuLxkqlqYw", "source": "YouTube", "title": "CITTA' '93 (2023, full album)"},
            {"url": "https://www.youtube.com/watch?v=FRyBDpYFF8I", "source": "YouTube", "title": "Club Citta 1993"},
            {"url": "https://www.youtube.com/watch?v=RrDv1lwv8mg", "source": "YouTube", "title": "1993-02-17 Club Citta, Tokyo"},
        ],
    },
    {
        "match_date": "1994-09-09",
        "match_location": "CITTA",
        "recordings": [
            {"url": "https://www.youtube.com/watch?v=3IURBxGP1V8", "source": "YouTube", "title": "LIVE 1994-09-09, CLUB CITTA' (remastered)"},
        ],
    },
]


def _match_text(show: dict) -> str:
    return f"{show['venue']} {show['place']}".lower()


def _attach_recordings(shows, rules):
    for show in shows:
        blob = _match_text(show)
        for rule in rules:
            if show["date"] != rule["match_date"]:
                continue
            if rule["match_location"].lower() not in blob:
                continue
            for rec in rule["recordings"]:
                if rec not in show["recordings"]:
                    show["recordings"].append(rec)


def build():
    shows = []
    for display, location in SETLIST_FM:
        iso, year = parse_date(display)
        shows.append(show_from_location(iso, year, location, source="setlist.fm"))

    for extra in SUPPLEMENTAL:
        entry = dict(extra)
        loc = entry.pop("location")
        shows.append(
            show_from_location(
                entry["date"],
                entry["year"],
                loc,
                notes=entry.get("notes"),
                source=entry.get("source"),
            )
        )

    _attach_recordings(shows, RECORDINGS)
    _attach_recordings(shows, YOUTUBE_RECORDINGS)

    shows.sort(key=lambda s: (s["date"], s["venue"], s["place"]))

    payload = json.dumps({"shows": shows}, indent=2, ensure_ascii=False) + "\n"

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(payload)

    PUBLIC_OUT.parent.mkdir(parents=True, exist_ok=True)
    PUBLIC_OUT.write_text(payload)

    print(f"Wrote {len(shows)} shows to {OUT} and {PUBLIC_OUT}")


if __name__ == "__main__":
    build()
