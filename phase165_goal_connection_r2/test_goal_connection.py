"""Focused tests for the explicit typed Goal -> common search connection."""
from types import SimpleNamespace

import pytest

from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from proof import Relation, RelationType


def _goal():
    eta = HomotopyElement(
        name="η_3", dimension=3, source=4, target=3,
        generator=GeneratorSymbol(family="η", index=3),
    )
    return Relation(
        TodaPrimaryGroup(4, 3), FiniteCyclicGroup(2, eta), RelationType.EQUALITY,
    )


def test_explicit_goal_reaches_common_search_without_registry_candidate(monkeypatch):
    import phase165_r55_nk_only_goal as module
    goal = _goal()
    passed = []

    def fake_search(**kwargs):
        passed.append(kwargs)
        return make_partial_proof_result(
            n=3, k=1, status=ProofSearchStatus.SEARCH_FAILED,
            open_goals=(goal,), diagnostics=("not proved",),
        )

    monkeypatch.setattr(module, "registered_group_goal_candidates", lambda *a, **k: pytest.fail("registry goal lookup must not run"))
    monkeypatch.setattr(module, "search_shared_group_goal", fake_search)
    result = search_group_from_registered_goal(
        n=3, k=1, bridge=SimpleNamespace(), proof_order_catalog=object(), goal=goal,
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.open_goals == (goal,)
    assert passed[0]["group_structure"] == goal.rhs
    assert result.proven_steps == ()


def test_wrong_dimension_goal_is_rejected():
    with pytest.raises(ValueError, match="typed equality"):
        search_group_from_registered_goal(
            n=4, k=1, bridge=SimpleNamespace(), proof_order_catalog=object(), goal=_goal(),
        )


def test_nk_only_path_remains_fail_closed(monkeypatch):
    import phase165_r55_nk_only_goal as module
    monkeypatch.setattr(module, "registered_group_goal_candidates", lambda *a, **k: ())
    result = search_group_from_registered_goal(
        n=3, k=1, bridge=SimpleNamespace(), proof_order_catalog=object(),
    )
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.proven_steps == ()
    assert result.open_goals == (TodaPrimaryGroup(4, 3),)
