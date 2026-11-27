"""Human-readable explanation of static scan findings."""
from sentinel.core.result_models import ScanResult
from sentinel.ai.analyst import Analyst

def explain(result: ScanResult) -> str:
    missing = "\nMissing evidence: reputation lookup and signature verification were not performed." if not result.evidence else ""
    return Analyst().summarize(result) + missing
