"""Hash-bound, explicit user trust decisions."""
from datetime import datetime, timezone
from sentinel.storage.database import Database

class TrustRepository:
    def __init__(self, database: Database) -> None: self.database = database
    def add(self, sha256: str, note: str = "") -> None:
        if not _valid_hash(sha256): raise ValueError("A valid SHA-256 hash is required.")
        with self.database.connect() as db:
            db.execute("INSERT INTO trust_records(sha256,note,created_at) VALUES(?,?,?) ON CONFLICT(sha256) DO UPDATE SET note=excluded.note", (sha256.lower(),note,datetime.now(timezone.utc).isoformat()))
    def revoke(self, sha256: str) -> bool:
        with self.database.connect() as db: return db.execute("DELETE FROM trust_records WHERE sha256=?", (sha256.lower(),)).rowcount > 0
    def list_all(self) -> list[dict]:
        with self.database.connect() as db: return [dict(row) for row in db.execute("SELECT id,sha256,note,created_at FROM trust_records ORDER BY id DESC").fetchall()]
    def contains(self, sha256: str) -> bool:
        with self.database.connect() as db: return db.execute("SELECT 1 FROM trust_records WHERE sha256=?",(sha256.lower(),)).fetchone() is not None

def _valid_hash(value: str) -> bool:
    return len(value)==64 and all(char in "0123456789abcdefABCDEF" for char in value)
