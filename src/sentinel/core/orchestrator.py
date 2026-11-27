"""Application analysis orchestration."""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from sentinel.core.file_identity import identify_file
from sentinel.core.result_models import AnalysisStatus, ScanResult
from sentinel.core.risk_engine import assess_risk
from sentinel.scanners.static_scanner import StaticScanner
from sentinel.storage.scan_repository import ScanRepository


class Orchestrator:
    def __init__(self, repository: ScanRepository | None = None) -> None:
        self.repository = repository
        self.scanner = StaticScanner()

    def analyze(self, path: str | Path) -> ScanResult:
        identity = identify_file(path)
        evidence = self.scanner.scan(identity)
        risk = assess_risk(evidence)
        status = AnalysisStatus.REVIEW_REQUIRED if risk in {"HIGH", "ELEVATED", "UNKNOWN"} else AnalysisStatus.COMPLETED
        result = ScanResult(
            identity=identity,
            status=status,
            risk=risk,
            evidence=evidence,
            limitations=[
                "Static inspection cannot establish file safety; no indicators observed is not a safety guarantee.",
                "Digital signature verification is unavailable in this build.",
                "No file contents were uploaded or executed.",
            ],
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        if self.repository:
            result.scan_id = self.repository.save(result)
        return result
