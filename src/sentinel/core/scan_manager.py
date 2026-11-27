"""Synchronous manager boundary, suitable for a UI worker or CLI."""
from pathlib import Path
from sentinel.core.orchestrator import Orchestrator
from sentinel.core.result_models import ScanResult

class ScanManager:
    def __init__(self, orchestrator: Orchestrator) -> None:
        self.orchestrator = orchestrator
    def scan(self, path: str | Path) -> ScanResult:
        return self.orchestrator.analyze(path)
