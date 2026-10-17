"""Targeted audit tests; production code is not modified."""
from phase165_rule_identity_r8.audit import classify_pair


def test_r8_pair_has_same_forward_patterns():
    result = classify_pair()
    assert result["same_premises"] is True
    assert result["same_conclusion"] is True


def test_r8_composition_rule_has_additional_guard():
    result = classify_pair()
    assert result["general_has_guard"] is False
    assert result["composition_has_guard"] is True
    assert result["classification"] == "SAME_PATTERNS_DIFFERENT_APPLICABILITY__KEEP_BOTH"
    assert result["removal_performed"] is False
