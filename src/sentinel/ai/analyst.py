"""Local deterministic evidence summarizer; no model or network call."""
from sentinel.core.result_models import ScanResult

class Analyst:
    def summarize(self, result: ScanResult) -> str:
        facts = "; ".join(item.title for item in result.evidence) or "No static indicators were produced"
        return f"Assessment: {result.risk}. Observed facts: {facts}. This assessment is limited to the evidence listed and is not a safety guarantee."
