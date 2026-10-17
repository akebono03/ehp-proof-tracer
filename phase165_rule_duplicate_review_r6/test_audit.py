"""Targeted checks, no full pytest run."""
from phase165_rule_duplicate_review_r6.audit import classify_pair, describe_rule, PAIRS


def test_distinct_conclusions_are_not_marked_duplicates():
    a = {"conclusion_type": "A", "conclusion_pattern": "A", "premises": []}
    b = {"conclusion_type": "B", "conclusion_pattern": "B", "premises": []}
    assert classify_pair(a, b) == "DIFFERENT_CONCLUSION_PATTERNS"


def test_missing_conclusion_patterns_are_not_certified_duplicates():
    a = {"conclusion_type": None, "conclusion_pattern": "None", "premises": []}
    assert classify_pair(a, a) == "NO_CONCLUSION_PATTERNS__NAME_AND_DESCRIPTION_REVIEW_REQUIRED"
    assert len(PAIRS) == 5
