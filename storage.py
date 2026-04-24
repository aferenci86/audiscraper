"""Tiny SQLite wrapper to track which listings we've already texted about."""
import sqlite3
import time
from config import DB_PATH


def init():
    con = sqlite3.connect(DB_PATH)
    con.execute("""
        CREATE TABLE IF NOT EXISTS seen (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            url TEXT NOT NULL,
            title TEXT,
            first_seen INTEGER NOT NULL
        )
    """)
    con.commit()
    con.close()


def is_new(listing_id: str) -> bool:
    con = sqlite3.connect(DB_PATH)
    cur = con.execute("SELECT 1 FROM seen WHERE id = ?", (listing_id,))
    hit = cur.fetchone() is not None
    con.close()
    return not hit


def mark_seen(listing_id: str, source: str, url: str, title: str):
    con = sqlite3.connect(DB_PATH)
    con.execute(
        "INSERT OR IGNORE INTO seen (id, source, url, title, first_seen) VALUES (?, ?, ?, ?, ?)",
        (listing_id, source, url, title, int(time.time())),
    )
    con.commit()
    con.close()
