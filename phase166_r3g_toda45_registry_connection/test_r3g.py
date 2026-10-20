"""R3-G focused registry, bidirectional specialization, and proof provenance tests."""
from expression import ScalarProduct, ScalarSum, ScalarSymbol
from homotopy_groups import TodaIteratedSuspensionMap, TodaPrimaryGroup
from phase165_r3_recursive_search import GoalExpansion
from phase165_r52_r27_r5_literature import build_typed_literature_bridge
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r57_r20_general_specialization import (
    expand_cited_general_specialization,
    specialize_typed_statement,
)
from phase165_r9_production_wiring import discover_goal_search_inputs
from proof import ProofRule, ProofStep, find_inference_match
from toda_rules import Toda45IsomorphismStatement
from unified_statement_registry import AssertionOrigin


def _concrete_iso(n: int, k: int, m: int) -> Toda45IsomorphismStatement:
    return Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
        exponent=m - n,
        source_group=TodaPrimaryGroup(group_dimension=n + k, sphere_dimension=n),
        target_group=TodaPrimaryGroup(group_dimension=m + k, sphere_dimension=m),
    ))


def _general(bridge):
    records = [a for a in bridge.registry._assertions.values()
               if isinstance(a.content, Toda45IsomorphismStatement)
               and isinstance(a.content.map.source_group.sphere_dimension, ScalarSymbol)]
    assert len(records) == 1
    return records[0]


def test_r3g_registry_has_single_typed_general_toda45_and_cited_given():
    bridge = build_typed_literature_bridge(discover_goal_search_inputs().bridge)
    entry = _general(bridge)
    assert bridge.registry.reference(entry.reference_id).locator == '(4.5)'
    assert entry.origin is AssertionOrigin.FIXED_STATEMENT
    assert entry.scope == ('n>=k+2', 'm>=n', 'k>=0')
    links = [link for link in bridge.proof_links if link.assertion_id == entry.assertion_id]
    assert len(links) == 1
    assert links[0].step.rule is ProofRule.GIVEN
    assert links[0].step.conclusion == entry.content
    assert isinstance(entry.content.map.exponent, ScalarSum)


def test_r3g_shared_registry_forward_and_backward_same_reference():
    bridge = build_shared_typed_bridge()
    entry = _general(bridge)
    goal = _concrete_iso(3, 1, 4)
    assert specialize_typed_statement(entry.content, goal) == (
        ('k', 1), ('m', 4), ('n', 3),
    )
    expansions = expand_cited_general_specialization(goal, (entry.content,))
    assert len(expansions) == 1
    assert expansions[0].subgoals == (entry.content,)
    original = next(link.step for link in bridge.proof_links
                    if link.assertion_id == entry.assertion_id)
    match = find_inference_match(expansions[0].rule, (original,))
    assert match is not None
    assert expansions[0].rule.conclusion_builder((original,)) == goal
    assert original.rule is ProofRule.GIVEN
    assert expansions[0].rule.name == 'generic cited typed scalar specialization'


def test_r3g_invalid_ranges_and_inconsistent_maps_never_specialize():
    general = _general(build_typed_literature_bridge(discover_goal_search_inputs().bridge)).content
    for (n, k, m) in ((3, 2, 4), (3, 1, 2), (4, -1, 5)):
        goal = _concrete_iso(n, k, m)
        assert specialize_typed_statement(general, goal) is None
        assert expand_cited_general_specialization(goal, (general,)) == ()
    incorrect = Toda45IsomorphismStatement(map=TodaIteratedSuspensionMap(
        exponent=2,
        source_group=TodaPrimaryGroup(group_dimension=4, sphere_dimension=3),
        target_group=TodaPrimaryGroup(group_dimension=5, sphere_dimension=4),
    ))
    assert specialize_typed_statement(general, incorrect) is None


def test_r3g_does_not_register_a_concrete_pi54_given():
    bridge = build_typed_literature_bridge(discover_goal_search_inputs().bridge)
    goal = _concrete_iso(3, 1, 4)
    assert all(link.step.conclusion != goal for link in bridge.proof_links)
    assert all(a.content != goal for a in bridge.registry._assertions.values())
