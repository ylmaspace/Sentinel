"""Fictional workflow display, never processes the sample."""
from sentinel.lab.lab_status import LAB_NOTICE

class SimulatedLab:
    def evaluate(self, sha256: str) -> dict[str, str]:
        return {"status": "SIMULATED", "sample": f"{sha256[:12]}…", "workflow": "Hypothetical isolation → observation → report", "result": "Fictional demonstration; no behavioral result", "notice": LAB_NOTICE}
