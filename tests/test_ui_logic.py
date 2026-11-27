from pathlib import Path
from sentinel.core.orchestrator import Orchestrator
from sentinel.integrations.virustotal import VirusTotalClient

def test_api_failure_is_unavailable_not_clean():
    result=VirusTotalClient().lookup_hash("a"*64)
    assert result.status == "UNAVAILABLE"
    assert "no request" in result.message

def test_scan_never_modifies_input(tmp_path: Path):
    f=tmp_path/"file.txt"; f.write_text("safe fixture",encoding="utf-8"); before=f.read_bytes()
    result=Orchestrator().analyze(f)
    assert f.read_bytes()==before
    assert "not a safety guarantee" in result.limitations[0]

def test_trust_does_not_suppress_scan(tmp_path: Path):
    from sentinel.storage.database import Database
    from sentinel.storage.trust_repository import TrustRepository
    from sentinel.storage.scan_repository import ScanRepository
    f=tmp_path/"same.bin"; f.write_bytes(b"data")
    db=Database(tmp_path/"db.sqlite"); db.initialize(); trust=TrustRepository(db)
    digest=Orchestrator().analyze(f).identity.sha256; trust.add(digest)
    result=Orchestrator(ScanRepository(db)).analyze(f)
    assert result.evidence and result.scan_id
