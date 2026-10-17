"""Focused tests for read-only rule inventory classification."""
from phase165_rule_registry_audit_r3.audit import classify_rule, KEYWORDS


def test_classification_distinguishes_not_discovered():
    assert classify_rule(implemented=True, discovered=False, pattern=None) == "IMPLEMENTED_NOT_DISCOVERED_BY_R8"
    assert classify_rule(implemented=False, discovered=False, pattern=None) == "NOT_FOUND_IN_SCANNED_MODULES"


def test_classification_distinguishes_reverse_pattern():
    assert classify_rule(implemented=True, discovered=True, pattern=False) == "DISCOVERED_WITHOUT_CONCLUSION_PATTERN"
    assert classify_rule(implemented=True, discovered=True, pattern=True) == "DISCOVERED_WITH_CONCLUSION_PATTERN"
    assert "kernel" in KEYWORDS and "surject" in KEYWORDS
