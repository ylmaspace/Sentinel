"""Persistence for scan history and evidence; file paths are deliberately not stored."""
from sentinel.storage.database import Database
from sentinel.core.result_models import ScanResult, Evidence

class ScanRepository:
    def __init__(self, database: Database) -> None: self.database = database
    def save(self, result: ScanResult) -> int:
        with self.database.connect() as db:
            cursor = db.execute("INSERT INTO scans(sha256,name,size,detected_type,status,risk,created_at) VALUES(?,?,?,?,?,?,?)", (result.identity.sha256, result.identity.name, result.identity.size, result.identity.detected_type, result.status.value, result.risk, result.created_at))
            scan_id = int(cursor.lastrowid)
            db.executemany("INSERT INTO evidence(scan_id,category,title,detail,severity,source) VALUES(?,?,?,?,?,?)", [(scan_id,e.category,e.title,e.detail,e.severity,e.source) for e in result.evidence])
            return scan_id
    def recent(self, limit: int = 50) -> list[dict]:
        with self.database.connect() as db:
            rows = db.execute("SELECT id,sha256,name,size,detected_type,status,risk,created_at FROM scans ORDER BY id DESC LIMIT ?", (max(1,min(limit,500)),)).fetchall()
            return [dict(row) for row in rows]
    def count(self) -> int:
        with self.database.connect() as db: return int(db.execute("SELECT COUNT(*) FROM scans").fetchone()[0])
