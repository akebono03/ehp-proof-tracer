"""Targeted checks for n,k-only selection and fail-closed search."""
from dataclasses import dataclass
from types import SimpleNamespace

import phase165_r55_nk_only_goal as selected
from expression import GeneratorSymbol, HomotopyElement
from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import GroupStructureStatus, ProofSearchStatus, make_partial_proof_result
from proof import Relation
from unified_statement_registry import AssertionOrigin


@dataclass(frozen=True)
class TypedComposite:
    group_relation: Relation


def _bridge_with(*contents):
    assertions = {
        str(i): SimpleNamespace(origin=AssertionOrigin.FIXED_STATEMENT, content=content)
        for i, content in enumerate(contents)
    }
    return SimpleNamespace(registry=SimpleNamespace(_assertions=assertions))


def _pi32():
    eta = HomotopyElement(name="η₂", dimension=2, source=3, target=2,
                          generator=GeneratorSymbol(family="η", index=2))
    return Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(eta))


def test_r55_discovers_group_goal_inside_fixed_typed_composite():
    goal = _pi32()
    assert selected.registered_group_goal_candidates(_bridge_with(TypedComposite(goal)), n=2, k=1) == (goal,)
    assert selected.registered_group_goal_candidates(_bridge_with(TypedComposite(goal)), n=3, k=1) == ()


def test_r55_calls_canonical_search_with_registered_goal_not_given(monkeypatch):
    goal = _pi32()
    observed = []
    monkeypatch.setattr(selected, "search_shared_group_goal", lambda **kw: (
        observed.append(kw), make_partial_proof_result(
            n=2, k=1, status=ProofSearchStatus.SEARCH_FAILED,
            diagnostics=("unresolved",), open_goals=(goal,),
        )
    )[1])
    result = selected.search_group_from_registered_goal(n=2, k=1, bridge=_bridge_with(TypedComposite(goal)))
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert len(observed) == 1
    assert observed[0]["group_structure"] == goal.rhs
    assert "completed_internal_proofs" not in observed[0]


def test_r55_no_candidates_fails_closed(monkeypatch):
    monkeypatch.setattr(selected, "search_shared_group_goal", lambda **kw: (_ for _ in ()).throw(AssertionError("unexpected search")))
    result = selected.search_group_from_registered_goal(n=3, k=1, bridge=_bridge_with())
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert result.open_goals
    assert not result.proven_steps


def test_r55_multiple_candidates_do_not_guess(monkeypatch):
    a = _pi32()
    b = Relation(a.lhs, FreeCyclicGroup(HomotopyElement(
        name="other", dimension=2, source=3, target=2,
        generator=GeneratorSymbol(family="x", index=2),
    )))
    monkeypatch.setattr(selected, "search_shared_group_goal", lambda **kw: (_ for _ in ()).throw(AssertionError("ambiguous")))
    result = selected.search_group_from_registered_goal(n=2, k=1, bridge=_bridge_with(a, b))
    assert result.status is ProofSearchStatus.SEARCH_FAILED
    assert "複数" in result.diagnostics[0]
