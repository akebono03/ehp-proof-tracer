from dataclasses import replace

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import Relation, RelationType
from unified_statement_registry import AssertionKind, AssertionOrigin, LiteratureEntry, ReferenceKind, AssertionEntry, UnifiedStatementRegistry
from phase163_r4_registry_bridge import RegistryBridgeResult


def _bridge(*, duplicate=False):
    registry = UnifiedStatementRegistry()
    registry.add_reference(LiteratureEntry(
        reference_id="source", kind=ReferenceKind.PROPOSITION,
        locator="Proposition 5.3", publication_position=8000,
    ))
    registry.add_assertion(AssertionEntry(
        assertion_id="group-pi42", reference_id="source",
        kind=AssertionKind.STATEMENT,
        content=Relation(
            TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
            FiniteCyclicGroup(order=2, generator="g"),
            relation_type=RelationType.EQUALITY,
        ),
        origin=AssertionOrigin.FIXED_STATEMENT,
        component_position=100,
    ))
    if duplicate:
        registry.add_assertion(AssertionEntry(
            assertion_id="same-group", reference_id="source",
            kind=AssertionKind.STATEMENT,
            content=Relation(
                TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
                FiniteCyclicGroup(order=2, generator="g"),
                relation_type=RelationType.EQUALITY,
            ),
            origin=AssertionOrigin.FIXED_STATEMENT,
            component_position=200,
        ))
    return RegistryBridgeResult(registry, (), ())


def test_dimension_and_group_content_find_positioned_claim():
    bridge = _bridge()
    goal = bridge.registry.assertion("group-pi42").content
    assert resolve_specialized_goal_citing_id(bridge, goal) == "group-pi42"


def test_same_dimension_wrong_group_does_not_bind():
    bridge = _bridge()
    goal = Relation(
        TodaPrimaryGroup(group_dimension=4, sphere_dimension=2),
        FiniteCyclicGroup(order=4, generator="g"),
        relation_type=RelationType.EQUALITY,
    )
    assert resolve_specialized_goal_citing_id(bridge, goal) is None


def test_ambiguous_positioned_claims_do_not_select_first():
    bridge = _bridge(duplicate=True)
    goal = bridge.registry.assertion("group-pi42").content
    assert resolve_specialized_goal_citing_id(bridge, goal) is None


def test_existing_pi54_citation_binding_is_preserved():
    from phase165_r55_nk_only_goal import registered_group_goal_candidates
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=1)
    assert len(goals) == 1
    assert resolve_specialized_goal_citing_id(bridge, goals[0]) == (
        "shared:2:toda:adopted:prop5.1:higher_eta_group_relation"
    )
