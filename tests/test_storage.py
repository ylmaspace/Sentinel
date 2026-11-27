"""Database initialization and persistence regression coverage."""
from sentinel.core.orchestrator import Orchestrator
from sentinel.storage.database import Database
from sentinel.storage.scan_repository import ScanRepository
from sentinel.storage.trust_repository import TrustRepository


def test_database_and_scan_storage(tmp_path):
    db = Database(tmp_path / "nested" / "test.db")
    db.initialize()
    sample = tmp_path / "hello.txt"
    sample.write_text("harmless", encoding="utf-8")
    repo = ScanRepository(db)
    result = Orchestrator(repo).analyze(sample)
    assert result.scan_id and repo.count() == 1
    assert repo.recent()[0]["name"] == "hello.txt"
    with db.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM evidence WHERE scan_id=?", (result.scan_id,)).fetchone()[0] >= 1
        assert conn.execute("PRAGMA foreign_key_check").fetchall() == []


def test_initialize_is_repeatable_and_keeps_data(tmp_path):
    db = Database(tmp_path / "repeat.db")
    db.initialize()
    TrustRepository(db).add("a" * 64, "preserve me")
    db.initialize()
    records = TrustRepository(db).list_all()
    assert len(records) == 1
    assert records[0]["note"] == "preserve me"


def test_trust_add_contains_revoke(tmp_path):
    db = Database(tmp_path / "test.db")
    db.initialize()
    repo = TrustRepository(db)
    digest = "a" * 64
    repo.add(digest, "reviewed by user")
    repo.add(digest, "updated note")  # same identity remains a single record
    assert repo.contains(digest)
    assert len(repo.list_all()) == 1
    assert repo.list_all()[0]["note"] == "updated note"
    assert repo.revoke(digest) and not repo.contains(digest)


def test_invalid_trust_hash(tmp_path):
    import pytest
    db = Database(tmp_path / "test.db")
    db.initialize()
    with pytest.raises(ValueError):
        TrustRepository(db).add("filename.exe")
