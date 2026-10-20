from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r12_r7_proof_order_guard import restrict_registered_ordered_claims
from phase165_r57_r8_eta_specialization import (
    _is_generic_eta_group_relation, specialize_eta_group_relation,
)
from phase165_prop51_claim_order import ordered_prop51_items, pi4_3_goal


def _higher(bridge):
    parents = [a for a in bridge.registry._assertions.values()
               if a.assertion_id.endswith(':toda:adopted:prop5.1:finite_dimensional')]
    assert len(parents) == 1
    parent = parents[0]
    item = ordered_prop51_items(parent.content)[4]
    assert item.position == 5
    assert _is_generic_eta_group_relation(item.statement)
    return parent, item.statement


def test_fifth_claim_specialized_goal_cannot_cite_own_symbolic_source():
    bridge = build_shared_typed_bridge()
    parent, statement = _higher(bridge)
    goal = specialize_eta_group_relation(statement, 4)
    restricted = restrict_registered_ordered_claims(bridge, goal)
    assert any(link.step.conclusion == statement for link in bridge.proof_links)
    assert all(link.step.conclusion != statement for link in restricted.proof_links)
    assert all(link.assertion_id != parent.assertion_id for link in restricted.proof_links)


def test_fifth_claim_specialization_at_n5_also_excludes_self():
    bridge = build_shared_typed_bridge()
    _parent, statement = _higher(bridge)
    goal = specialize_eta_group_relation(statement, 5)
    restricted = restrict_registered_ordered_claims(bridge, goal)
    assert all(link.step.conclusion != statement for link in restricted.proof_links)


def test_pi43_keeps_preceding_delta_source():
    bridge = build_shared_typed_bridge()
    parent, _statement = _higher(bridge)
    restricted = restrict_registered_ordered_claims(bridge, pi4_3_goal())
    delta = parent.content.delta_iota5_relation
    assert any(link.step.conclusion == delta for link in restricted.proof_links)


def test_non_prop51_goal_does_not_gain_new_sources():
    bridge = build_shared_typed_bridge()
    _parent, statement = _higher(bridge)
    unrelated = object()
    restricted = restrict_registered_ordered_claims(bridge, unrelated)
    assert len(restricted.proof_links) == len(bridge.proof_links)
