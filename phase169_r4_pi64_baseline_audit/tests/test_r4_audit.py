"""Focused, read-only R4 audit contract tests (do not claim group proofs)."""
from __future__ import annotations

from types import SimpleNamespace

from phase169_r4_pi64_baseline_audit.audit import describe_search, stable_range_allows


def test_r4_toda45_source_below_stable_range():
    assert stable_range_allows(3, 2) is False


def test_r4_toda45_next_source_is_in_stable_range():
    assert stable_range_allows(4, 2) is True


def test_r4_stable_range_does_not_accept_bool_as_dimension():
    assert stable_range_allows(True, 2) is False
    assert stable_range_allows(4, True) is False


def test_r4_incomplete_search_never_infers_conclusion():
    result = SimpleNamespace(
        status=SimpleNamespace(value="partial"),
        proven_steps=(), open_goals=("goal",),
        diagnostics=("unresolved",), conclusion=None,
    )
    row = describe_search(result)
    assert row["status"] == "partial"
    assert row["has_root_in_proven_steps"] is False
    assert row["open_goals"] == ["'goal'"]
