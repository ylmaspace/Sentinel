"""SQLite lifecycle, schema migrations and transaction safety."""
from __future__ import annotations

import sqlite3
from pathlib import Path

SCHEMA_VERSION = 1


class Database:
    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA busy_timeout = 10000")
        return connection

    def initialize(self) -> None:
        """Create the current schema atomically, retaining compatible existing data."""
        with self.connect() as db:
            db.execute("BEGIN IMMEDIATE")
            # Execute statements individually: sqlite3.executescript() implicitly
            # commits pending transactions and would defeat this atomic setup.
            statements = (
                "CREATE TABLE IF NOT EXISTS schema_version (version INTEGER NOT NULL)",
                "CREATE TABLE IF NOT EXISTS scans (id INTEGER PRIMARY KEY, sha256 TEXT NOT NULL, name TEXT NOT NULL, size INTEGER NOT NULL, detected_type TEXT NOT NULL, status TEXT NOT NULL, risk TEXT NOT NULL, created_at TEXT NOT NULL)",
                "CREATE TABLE IF NOT EXISTS evidence (id INTEGER PRIMARY KEY, scan_id INTEGER NOT NULL REFERENCES scans(id) ON DELETE CASCADE, category TEXT NOT NULL, title TEXT NOT NULL, detail TEXT NOT NULL, severity TEXT NOT NULL, source TEXT NOT NULL)",
                "CREATE TABLE IF NOT EXISTS trust_records (id INTEGER PRIMARY KEY, sha256 TEXT NOT NULL UNIQUE, note TEXT NOT NULL DEFAULT '', created_at TEXT NOT NULL)",
                "CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL)",
                "CREATE INDEX IF NOT EXISTS idx_scans_created_at ON scans(created_at DESC)",
                "CREATE INDEX IF NOT EXISTS idx_scans_sha256 ON scans(sha256)",
                "CREATE INDEX IF NOT EXISTS idx_evidence_scan_id ON evidence(scan_id)",
            )
            for statement in statements:
                db.execute(statement)

            row = db.execute("SELECT MAX(version) AS version FROM schema_version").fetchone()
            current = int(row["version"] or 0)
            if current == 0:
                db.execute("INSERT INTO schema_version(version) VALUES (?)", (SCHEMA_VERSION,))
            elif current != SCHEMA_VERSION:
                raise sqlite3.DatabaseError(
                    f"Unsupported schema version {current}; Sentinel cannot safely migrate it."
                )
