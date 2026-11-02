"""Focused regression contracts for the Phase 173 R4-R9 read-only audit."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaPrimaryGroupZeroStatement
from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r9_generalization_audit.audit import inspect_dimension


@pytest.mark.parametrize("dimension", (7, 8, 9, 10, 11, 12))
def test_frontier_inspection_never_claims_a_proof(dimension: int) -> None:
    row = inspect_dimension(dimension)
    assert row["dimension"] == dimension
    assert row["k"] == dimension - 4
    assert row["proof_certified_by_this_audit"] is False
    assert isinstance(row["unresolved_implementation_conditions"], list)


def test_existing_bounded_rules_are_recorded_without_rewriting() -> None:
    assert inspect_dimension(7)["bounded_source_first_rule_accepts"] is False
    for dimension in (8, 9, 10):
        row = inspect_dimension(dimension)
        assert row["bounded_source_first_rule_accepts"] is True
        assert row["generator_image_shape_matches"] is True


def test_pi11_zero_goal_is_detected_but_not_converted_to_axiom() -> None:
    goal = exact_prior_database_result(4, 7)
    assert isinstance(goal, TodaPrimaryGroupZeroStatement)
    row = inspect_dimension(11)
    assert row["target_type"] == "TodaPrimaryGroupZeroStatement"
    assert row["bounded_source_first_rule_accepts"] is False
    assert "zero_goal_bypasses_shared_group_goal_public_route" in row[
        "unresolved_implementation_conditions"
    ]


def test_pi12_unverified_generator_image_must_not_certify_a_proof() -> None:
    row = inspect_dimension(12)
    assert row["bounded_source_first_rule_accepts"] is False
    assert row["proof_certified_by_this_audit"] is False
    assert "source_first_screen_and_public_route_currently_exclude_this_target" in row[
        "unresolved_implementation_conditions"
    ]
