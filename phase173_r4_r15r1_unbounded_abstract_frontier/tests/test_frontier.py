"""Focused repository-backed, mathematical-structure-only tests."""
from __future__ import annotations

from dataclasses import replace

import pytest

from phase169_r10e4_ordered_db_prior.db_prior import exact_prior_database_result
from phase173_r4_r10_general_toda56_core.core import (
    checked_abstract_inputs,
    checked_general_inputs,
)
from phase173_r4_r15r1_unbounded_abstract_frontier.frontier import inspect_k


@pytest.mark.parametrize("k", (3, 4, 5, 6, 7))
def test_prior_signature_previously_proven_dimensions(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    assert checked_abstract_inputs(goal) is not None


def test_k31_abstract_prior_gate_is_generic_but_named_generator_is_not_certified() -> None:
    goal = exact_prior_database_result(4, 31)
    assert goal is not None
    prior = checked_abstract_inputs(goal)
    assert prior is not None
    assert prior[0] == exact_prior_database_result(3, 31)
    assert prior[1] == exact_prior_database_result(7, 28)
    assert checked_general_inputs(goal) is None
    row = inspect_k(31)
    assert row["target_signature"] == (("finite", 2),) * 8
    assert row["first_signature"] == (("finite", 2),) * 4
    assert row["second_signature"] == (("finite", 2),) * 4
    assert row["frontier"] == "GENERATOR_IMAGE_PROOF_PENDING"
    assert row["public_proof_complete_by_this_change"] is False


def test_existing_strict_generator_guards_retained() -> None:
    for k in (4, 5, 6, 7):
        goal = exact_prior_database_result(4, k)
        assert checked_general_inputs(goal) is not None
    goal12 = exact_prior_database_result(4, 8)
    assert goal12 is not None
    assert checked_general_inputs(goal12) is None
    legacy = exact_prior_database_result(4, 3)
    assert checked_general_inputs(legacy) is None


def test_forged_registered_group_is_not_admitted() -> None:
    goal = exact_prior_database_result(4, 31)
    assert goal is not None
    altered = replace(goal, rhs=exact_prior_database_result(4, 4).rhs)
    assert checked_abstract_inputs(altered) is None


def test_invalid_k_rejected_before_reading_database() -> None:
    with pytest.raises(ValueError):
        inspect_k(2)
    with pytest.raises(ValueError):
        inspect_k(True)
