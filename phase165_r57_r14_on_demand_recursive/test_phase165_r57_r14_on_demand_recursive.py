"""R57-R14: actual on-demand recursion, not stored proof replay."""
import pytest

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase165_r57_r13_proof_order_catalog import ProofOrderCatalog, ProofOrderRecord
from phase165_r57_r14_recursive_search import search_recursively_in_proof_order
from proof import InferenceRule, PremisePattern, ProofRule, ProofStep, Relation, RelationType


def _target(n):
    return Relation(TodaPrimaryGroup(n + 1, n), FreeCyclicGroup(generator="formal-generator-" + str(n)), RelationType.EQUALITY)


def _catalog():
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord(_target(2), 1))
    catalog.register(ProofOrderRecord(_target(3), 2))
    catalog.register(ProofOrderRecord(_target(4), 3))
    return catalog


def _result(statement, complete):
    n = statement.lhs.sphere_dimension
    if not complete:
        return make_partial_proof_result(n=n, k=1, status=ProofSearchStatus.SEARCH_FAILED,
                                         open_goals=(statement,), diagnostics=("not proved",))
    premise = ProofStep(conclusion="independent-source-" + str(n), premises=(), rule=ProofRule.GIVEN)
    rule = InferenceRule(name="test inference", premise_patterns=(PremisePattern(statement_type=str),),
                         conclusion_builder=lambda steps: statement)
    root = ProofStep(conclusion=statement, premises=(premise,), rule=ProofRule.INFERENCE,
                     inference_rule=rule)
    return make_partial_proof_result(n=n, k=1, status=ProofSearchStatus.COMPLETE,
                                     proven_steps=(premise, root), conclusion=statement)


def test_r14_generates_all_earlier_goals_before_target_without_persisting():
    catalog = _catalog()
    seen = []

    def search(goal, prior, position):
        seen.append((position, tuple(item.order for item in prior)))
        return _result(goal, True)

    result = search_recursively_in_proof_order(catalog, _target(4), search)
    assert result.status is ProofSearchStatus.COMPLETE
    assert seen == [(1, ()), (2, (1,)), (3, (1, 2))]
    assert all(record.completed is None for record in catalog._records)


def test_r14_does_not_reuse_failed_predecessor():
    seen = []

    def search(goal, prior, position):
        seen.append((position, tuple(item.order for item in prior)))
        return _result(goal, position != 2)

    search_recursively_in_proof_order(_catalog(), _target(4), search)
    assert seen == [(1, ()), (2, (1,)), (3, (1,))]


def test_r14_recomputes_proofs_for_each_request():
    calls = []

    def search(goal, prior, position):
        calls.append(position)
        return _result(goal, True)

    catalog = _catalog()
    search_recursively_in_proof_order(catalog, _target(4), search)
    search_recursively_in_proof_order(catalog, _target(4), search)
    assert calls == [1, 2, 3, 1, 2, 3]


def test_r14_rejects_persisted_roots_and_unknown_order():
    from phase165_r52_r17_internal_dependency import CompletedInternalProof
    previously = _result(_target(2), True)
    catalog = ProofOrderCatalog()
    catalog.register(ProofOrderRecord(_target(2), 1, CompletedInternalProof(previously.proven_steps[-1])))
    catalog.register(ProofOrderRecord(_target(3), 2))
    with pytest.raises(ValueError, match="forbids registered completed proofs"):
        search_recursively_in_proof_order(catalog, _target(3), lambda goal, prior, order: _result(goal, True))
    with pytest.raises(ValueError, match="registered proof order"):
        search_recursively_in_proof_order(_catalog(), _target(9), lambda goal, prior, order: _result(goal, True))


def test_r14_rejects_fake_completed_root():
    def fake(goal, prior, position):
        n = goal.lhs.sphere_dimension
        leaf = ProofStep(conclusion=goal, premises=(), rule=ProofRule.GIVEN)
        return make_partial_proof_result(n=n, k=1, status=ProofSearchStatus.COMPLETE,
                                         proven_steps=(leaf,), conclusion=goal)

    with pytest.raises(ValueError, match="inferred root"):
        search_recursively_in_proof_order(_catalog(), _target(4), fake)


def test_r14_shared_entry_exposes_on_demand_mode():
    from inspect import signature
    from phase165_r52_r9_shared_math import search_shared_group_goal
    assert "recursive_proof_order_catalog" in signature(search_shared_group_goal).parameters
