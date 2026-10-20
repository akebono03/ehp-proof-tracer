from types import SimpleNamespace
from unittest.mock import patch

from homotopy_groups import FreeCyclicGroup, TodaPrimaryGroup
from hopf_facts import ETA_2
from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r55_nk_only_goal import _r3q_publication_boundary, search_group_from_registered_goal
from proof import Relation
from unified_statement_registry import AssertionEntry, AssertionKind, AssertionOrigin, LiteratureEntry, ReferenceKind, UnifiedStatementRegistry


def _bridge(candidate, *, duplicated=False, unlocated=False):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry('earlier', ReferenceKind.EQUATION, 'Earlier', publication_position=10))
    registry.add_reference(LiteratureEntry('target', ReferenceKind.PROPOSITION, 'Target', publication_position=None if unlocated else 20))
    registry.add_assertion(AssertionEntry('earlier-a', 'earlier', AssertionKind.STATEMENT, 'prior', origin=AssertionOrigin.FIXED_STATEMENT, component_position=100))
    registry.add_assertion(AssertionEntry('target-a', 'target', AssertionKind.STATEMENT, candidate, origin=AssertionOrigin.FIXED_STATEMENT, component_position=100))
    if duplicated:
        registry.add_assertion(AssertionEntry('target-b', 'target', AssertionKind.STATEMENT, (candidate,), origin=AssertionOrigin.FIXED_STATEMENT, component_position=200))
    return RegistryBridgeResult(registry, (), ())


def test_r3q_unique_printed_target_uses_existing_order():
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    assert _r3q_publication_boundary(_bridge(goal), goal) == 'target-a'


def test_r3q_ambiguous_target_does_not_invent_boundary():
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    assert _r3q_publication_boundary(_bridge(goal, duplicated=True), goal) is None


def test_r3q_unlocated_target_does_not_invent_boundary():
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    assert _r3q_publication_boundary(_bridge(goal, unlocated=True), goal) is None


def test_r3q_ordinary_call_keeps_goal_separate_from_boundary():
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    bridge = _bridge(goal)
    result = SimpleNamespace(status=None, conclusion=None)
    with patch('phase165_r55_nk_only_goal.search_shared_group_goal', return_value=result) as search:
        assert search_group_from_registered_goal(n=2, k=1, bridge=bridge, goal=goal, proof_order_catalog=SimpleNamespace()) is result
    assert search.call_args.kwargs['citing_assertion_id'] == 'target-a'


def test_r3q_unlocated_ordinary_call_preserves_legacy_entry():
    goal = Relation(TodaPrimaryGroup(3, 2), FreeCyclicGroup(ETA_2))
    bridge = _bridge(goal, unlocated=True)
    result = SimpleNamespace(status=None, conclusion=None)
    with patch('phase165_r55_nk_only_goal.search_shared_group_goal', return_value=result) as search:
        assert search_group_from_registered_goal(n=2, k=1, bridge=bridge, goal=goal, proof_order_catalog=SimpleNamespace()) is result
    assert 'citing_assertion_id' not in search.call_args.kwargs
