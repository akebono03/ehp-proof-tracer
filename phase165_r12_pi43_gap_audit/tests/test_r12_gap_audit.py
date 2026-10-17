from audit import make_report


def test_rule_registry_and_provider_share_inventory():
    report = make_report()
    assert report["registered_rule_count"] == report["provider_rule_count"]
    assert report["registered_rule_count"] > 0


def test_audit_does_not_claim_proof():
    report = make_report()
    assert report["proof_generated"] is False
    assert report["proofstep_verified"] is False
    assert report["full_pytest_run"] is False


def test_relevant_rules_are_registered():
    report = make_report()
    assert all(item["rule_id"] and item["name"] for item in report["relevant_rules"])
