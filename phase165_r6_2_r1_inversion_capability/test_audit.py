from audit import NAMES,inspect_rule,make_report

def test_all_required_rules_reported():
    report=make_report()
    assert [r["name"] for r in report["rules"]]==list(NAMES)
    assert all(isinstance(row["invertible"],bool) for row in report["rules"])

def test_does_not_claim_malformed_factory_is_invertible():
    assert not inspect_rule("nonexistent_factory_name")["invertible"]
