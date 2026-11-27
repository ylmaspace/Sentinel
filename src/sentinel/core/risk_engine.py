"""Evidence-based conservative risk assessment."""
from sentinel.core.result_models import Evidence

def assess_risk(evidence: list[Evidence], *, incomplete: bool = False) -> str:
    """Assess only the supplied evidence; absence of evidence is not a clean verdict."""
    severities = {item.severity.lower() for item in evidence}
    if "critical" in severities or "high" in severities:
        return "HIGH"
    if "medium" in severities:
        return "ELEVATED"
    if incomplete or not evidence:
        return "UNKNOWN"
    return "NO INDICATORS OBSERVED"
