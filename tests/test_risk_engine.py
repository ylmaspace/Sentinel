from sentinel.core.result_models import Evidence
from sentinel.core.risk_engine import assess_risk

def test_no_evidence_is_unknown(): assert assess_risk([]) == "UNKNOWN"
def test_incomplete_is_unknown(): assert assess_risk([Evidence("x","fact","seen")],incomplete=True) == "UNKNOWN"
def test_risk_uses_severity():
    assert assess_risk([Evidence("x","fact","seen","medium")]) == "ELEVATED"
    assert assess_risk([Evidence("x","fact","seen","high")]) == "HIGH"
def test_info_is_not_a_clean_guarantee(): assert assess_risk([Evidence("x","hash","calculated")]) == "NO INDICATORS OBSERVED"
