"""SQLite lifecycle and versioned schema."""
from __future__ import annotations
import sqlite3
from pathlib import Path

class Database:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
    def initialize(self) -> None:
        with self.connect() as db:
            db.executescript("""
                CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL);
                INSERT INTO schema_version(version) SELECT 1 WHERE NOT EXISTS (SELECT 1 FROM schema_version);
                CREATE TABLE IF NOT EXISTS scans (id INTEGER PRIMARY KEY, sha256 TEXT NOT NULL, name TEXT NOT NULL, size INTEGER NOT NULL, detected_type TEXT NOT NULL, status TEXT NOT NULL, risk TEXT NOT NULL, created_at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS evidence (id INTEGER PRIMARY KEY, scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE, category TEXT NOT NULL, title TEXT NOT NULL, detail TEXT NOT NULL, severity TEXT NOT NULL, source TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS trust_records (id INTEGER PRIMARY KEY, sha256 TEXT NOT NULL UNIQUE, note TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            """)
