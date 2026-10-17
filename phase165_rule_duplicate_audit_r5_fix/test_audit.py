"""Targeted tests for the active R8 read-only rule duplicate audit."""
from phase165_rule_duplicate_audit_r5_fix.audit import (
    REMOVED_RULE_NAMES,
    grouping,
    main,
)


def test_grouping_identifies_repeated_names_only():
    records = [
        ("r1", "same", "a", 1),
        ("r2", "same", "b", 2),
        ("r3", "other", "a", 3),
    ]
    assert grouping(records, 1) == [["r1", "r2"]]
    assert grouping(records, 2) == [["r1", "r3"]]


def test_active_discovery_does_not_reintroduce_removed_pi43_rules():
    result = main()
    assert result["retired_catalog_called"] is False
    assert result["dedicated_pi43_names_discovered"] == []
    assert result["discovered_rules"] >= 0
    assert REMOVED_RULE_NAMES
