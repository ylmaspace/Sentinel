"""Integration selection. External reputation checks are disabled unless explicitly supplied."""
from sentinel.integrations.external_sources import SimulatedReputationProvider

class IntegrationManager:
    def __init__(self, provider=None) -> None:
        self.provider = provider or SimulatedReputationProvider()
    def lookup_hash(self, sha256: str):
        return self.provider.lookup_hash(sha256)
