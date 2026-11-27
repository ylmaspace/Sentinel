"""Centralized product safety restrictions."""
from dataclasses import dataclass

@dataclass(frozen=True)
class PolicyDecision:
    allowed: bool
    reason: str

class PolicyEngine:
    """Explicitly deny actions outside Sentinel's analysis-only purpose."""
    DENIED = {"execute", "delete", "quarantine", "modify", "block", "upload_file", "auto_trust", "defender_change", "persistence"}
    def evaluate(self, action: str) -> PolicyDecision:
        normalized = action.strip().lower()
        if normalized in self.DENIED:
            return PolicyDecision(False, f"'{normalized}' is prohibited by Sentinel's safety policy.")
        if normalized in {"hash", "read_metadata", "static_scan", "hash_lookup", "add_trust_with_confirmation", "revoke_trust"}:
            return PolicyDecision(True, "Allowed as a user-controlled analysis or registry action.")
        return PolicyDecision(False, "Unknown actions are denied by default.")
