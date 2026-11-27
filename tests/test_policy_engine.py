from sentinel.core.policy_engine import PolicyEngine

def test_restricts_dangerous_actions():
    engine=PolicyEngine()
    for action in ("execute","delete","quarantine","modify","block","upload_file","auto_trust","defender_change","persistence"):
        assert not engine.evaluate(action).allowed

def test_unknown_denied_and_hash_allowed():
    engine=PolicyEngine()
    assert not engine.evaluate("whatever").allowed
    assert engine.evaluate("hash").allowed
