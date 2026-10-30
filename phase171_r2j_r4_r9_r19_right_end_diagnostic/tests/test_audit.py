"""Focused read-only right-end group diagnostics and classification tests."""
from __future__ import annotations

import pytest

from phase171_r2j_r4_r9_r19_right_end_diagnostic.audit import (
    classify_right_failure,
    describe_route,
    exact_screened_sources,
)
from phase165_r3_recursive_search import GoalExpansion
from proof import Relation, RelationType


def test_missing_source_and_empty_provider_is_not_proved():
    assert classify_right_failure(
        status="unresolved", route_names=(), exact_leaf_count=0,
        eta_source_count=0, eta_route_count=0, error="found 0",
    ) == "RIGHT_GROUP_NO_PROVIDER_EXPANSION"


def test_existing_eta_source_but_missing_route_is_distinguished():
    assert classify_right_failure(
        status="unresolved", route_names=("candidate",), exact_leaf_count=0,
        eta_source_count=1, eta_route_count=0, error="found 0",
    ) == "RIGHT_GROUP_ETA_SOURCE_PRESENT_ROUTE_MISSING"


def test_cited_source_absence_is_not_filled_by_a_fake_given():
    assert classify_right_failure(
        status="unresolved", route_names=("candidate",), exact_leaf_count=0,
        eta_source_count=0, eta_route_count=0, error="found 0",
    ) == "RIGHT_GROUP_CITED_SOURCE_NOT_AVAILABLE"


def test_ambiguous_derivation_is_not_treated_as_completion():
    assert classify_right_failure(
        status="unresolved", route_names=("a", "b"), exact_leaf_count=1,
        eta_source_count=1, eta_route_count=1,
        error="expected one registered derivation, found 2",
    ) == "RIGHT_GROUP_AMBIGUOUS_DERIVATIONS"


def test_proposal_representation_is_only_a_backward_obligation():
    from proof import InferenceRule
    proposed = GoalExpansion(InferenceRule(name="sample"), (
        Relation("x", "y", RelationType.EQUALITY),
    ))
    row = describe_route(proposed)
    assert row["rule"] == "sample"
    assert row["subgoals"] == [repr(proposed.subgoals[0])]


def test_read_only_git_guard_rejects_mutating_command():
    from phase171_r2j_r4_r9_r16_hopf_route_audit.audit import git_read
    with pytest.raises(ValueError):
        git_read("reset", "--hard")


def test_live_screened_source_search_rejects_unrelated_goal():
    from phase171_r2i_eta_hopf_bridge.audit import _screened_context
    bridge, _, citing = _screened_context()
    assert exact_screened_sources(object(), bridge, citing) == []
