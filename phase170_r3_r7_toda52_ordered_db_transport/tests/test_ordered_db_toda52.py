"""Focused real-repository checks for generalized Toda (5.2) and DB precedence."""
from __future__ import annotations

from types import SimpleNamespace

import pytest

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaPrimaryGroupZeroStatement
from phase165_r52_r27_r5_literature import Toda52UniversalStatement
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase166_r3af_goal_adapter import database_zero_group_goal_candidates
from phase169_r10e4_ordered_db_prior.db_prior import (
    admitted_db_step, exact_prior_database_result, group_coordinates, precedes_db_goal,
)
from phase168_r2_toda52_transport import (
    _toda52_group_presentation_matches, expand_toda52_finite_cyclic_goal,
)
from proof import Relation, RelationType


def _db_goal(k: int) -> object:
    zeros = database_zero_group_goal_candidates(n=2, k=k)
    if zeros:
        assert len(zeros) == 1
        return zeros[0]
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=k)
    assert len(goals) == 1
    return goals[0]


@pytest.mark.parametrize("k", [4, 6, 7, 8, 9, 10, 14])
def test_r3r7_db_source_precedes_and_is_a_typed_eta2_presentation(k: int) -> None:
    target = _db_goal(k)
    dimension = k + 2
    source = exact_prior_database_result(3, dimension - 3)
    assert source is not None
    assert group_coordinates(source) == (3, k - 1)
    assert precedes_db_goal(3, k - 1, 2, k)
    assert _toda52_group_presentation_matches(source, target)
    assert admitted_db_step(source, proof_target=target) is not None


@pytest.mark.parametrize("k", [4, 6, 7, 8, 9, 10, 14])
def test_r3r7_inference_requests_db_source_and_cited_theorem(k: int) -> None:
    target = _db_goal(k)
    theorem = Toda52UniversalStatement()
    proposals = expand_toda52_finite_cyclic_goal(target, (theorem,))
    assert len(proposals) == 1
    source, citation = proposals[0].subgoals
    assert group_coordinates(source) == (3, k - 1)
    assert citation == theorem
    assert proposals[0].rule.match_guard(
        (SimpleNamespace(conclusion=source), SimpleNamespace(conclusion=theorem)),
        {},
    )
    assert expand_toda52_finite_cyclic_goal(target, ()) == ()
    assert not proposals[0].rule.match_guard(
        (SimpleNamespace(conclusion=target), SimpleNamespace(conclusion=theorem)),
        {},
    )


def test_r3r7_does_not_create_source_as_an_unproved_root() -> None:
    target = _db_goal(6)
    assert isinstance(target, Relation)
    assert target.lhs == TodaPrimaryGroup(8, 2)
    wrong = Relation(
        target.lhs,
        FiniteCyclicGroup(7, target.rhs.generator),
        RelationType.EQUALITY,
    )
    assert expand_toda52_finite_cyclic_goal(
        wrong, (Toda52UniversalStatement(),),
    ) == ()


def test_r3r7_zero_is_typed_without_generator_invention() -> None:
    target = _db_goal(7)
    assert isinstance(target, TodaPrimaryGroupZeroStatement)
    source = exact_prior_database_result(3, 6)
    assert isinstance(source, TodaPrimaryGroupZeroStatement)
    assert source.group == TodaPrimaryGroup(9, 3)
    assert _toda52_group_presentation_matches(source, target)
