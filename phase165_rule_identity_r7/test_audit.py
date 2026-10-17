"""Only targeted audit tests; no full pytest."""
from phase165_rule_identity_r7.audit import PAIRS, classify_pair, main


def test_review_pair_inventory_has_five_unique_pairs():
    assert len(PAIRS) == 5
    assert len(set(PAIRS)) == 5


def test_review_preserves_rules_and_reports_five_pairs():
    result = main()
    assert result["pairs_reviewed"] == 5
    assert not result["retired_catalog_called"]
    assert not result["production_modified"]
    assert all("classification" in p for p in result["pairs"])
