"""Focused read-only duplicate-inventory audit tests."""
from phase165_rule_duplicate_audit_r5.audit import main


def test_catalog_keys_are_unique():
    result = main()
    assert result['catalog_unique_keys'] == result['catalog_entries']


def test_no_removed_pi43_dedicated_rule_names():
    result = main()
    assert result['dedicated_pi43_names_in_catalog'] == []
