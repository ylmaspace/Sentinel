from sentinel.storage.database import Database
from sentinel.storage.scan_repository import ScanRepository
from sentinel.storage.trust_repository import TrustRepository
from sentinel.core.orchestrator import Orchestrator

def test_database_and_scan_storage(tmp_path):
    db=Database(tmp_path/"nested"/"test.db"); db.initialize()
    sample=tmp_path/"hello.txt"; sample.write_text("harmless",encoding="utf-8")
    repo=ScanRepository(db); result=Orchestrator(repo).analyze(sample)
    assert result.scan_id and repo.count()==1 and repo.recent()[0]["name"]=="hello.txt"
    with db.connect() as conn:
        assert conn.execute("SELECT COUNT(*) FROM evidence WHERE scan_id=?",(result.scan_id,)).fetchone()[0]>=1

def test_trust_add_contains_revoke(tmp_path):
    db=Database(tmp_path/"test.db"); db.initialize(); repo=TrustRepository(db); digest="a"*64
    repo.add(digest,"reviewed by user"); assert repo.contains(digest)
    assert repo.list_all()[0]["sha256"]==digest
    assert repo.revoke(digest) and not repo.contains(digest)

def test_invalid_trust_hash(tmp_path):
    import pytest
    db=Database(tmp_path/"test.db"); db.initialize()
    with pytest.raises(ValueError): TrustRepository(db).add("filename.exe")
