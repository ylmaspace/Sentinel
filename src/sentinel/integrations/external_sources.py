"""Provider interfaces for reputation integrations."""
from typing import Protocol
from sentinel.core.result_models import ReputationResult

class ReputationProvider(Protocol):
    def lookup_hash(self, sha256: str) -> ReputationResult: ...

class SimulatedReputationProvider:
    """Clearly fictional/offline provider used when no service is configured."""
    def lookup_hash(self, sha256: str) -> ReputationResult:
        from datetime import datetime, timezone
        return ReputationResult("SIMULATED", "Sentinel demonstration (not a real reputation source)", datetime.now(timezone.utc).isoformat(), message=f"No external lookup performed for {sha256[:12]}…")
