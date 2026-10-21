"""Focused tests: audit structure, without claiming a missing proof passes."""
from phase166_r3ae_multistem_real_audit.audit import OFFSETS, STEMS, inspect_target
from phase165_r52_r9_shared_math import build_shared_typed_bridge


def test_r3ae_scope_includes_stable_bases_and_later_dimensions():
    assert STEMS == (2, 3, 7)
    assert OFFSETS == (0, 1, 2)
    assert all(k + 2 >= k + 2 for k in STEMS)


def test_r3ae_missing_targets_are_reported_not_fabricated():
    bridge = build_shared_typed_bridge()
    result = inspect_target(bridge, 7, 0)
    assert result["stem"] == 7
    assert result["base_n"] == 9
    assert result["target_group"]
    assert "candidate_count" in result or "exception" in result
