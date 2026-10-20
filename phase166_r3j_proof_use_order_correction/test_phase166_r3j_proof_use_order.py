"""Focused checks for the user-agreed Proposition 5.1 proof-use positions."""
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_prop51_claim_order import proof_ordered_prop51_items
from proof import ProofRule


def test_r3j_five_typed_clauses_use_agreed_proof_order():
    bridge = build_adopted_prop51_reference()
    entries = {
        assertion.assertion_id.rsplit(':', 1)[-1]: assertion
        for assertion in bridge.registry._assertions.values()
        if assertion.component_position is not None
    }
    assert entries['eta2_hopf_relation'].component_position == 1
    assert entries['pi3_2_group_relation'].component_position == 2
    assert entries['delta_iota5_relation'].component_position == 3
    assert entries['pi4_3'].component_position == 4
    assert entries['higher_eta_group_relation'].component_position == 5
    assert len(entries) == 5


def test_r3j_ordered_items_follow_same_positions_as_registry():
    bridge = build_adopted_prop51_reference()
    content = bridge.registry.assertion('toda:adopted:prop5.1:finite_dimensional').content
    items = proof_ordered_prop51_items(content)
    assert [item.component_key for item in items] == [
        'eta2_hopf_relation', 'pi3_2_group_relation',
        'delta_iota5_relation', 'pi4_3_group_relation', 'higher_eta_group_relation',
    ]
    assert [item.position for item in items] == [1, 2, 3, 4, 5]


def test_r3j_registry_target_has_no_manual_given_link():
    bridge = build_adopted_prop51_reference()
    ids = {a.assertion_id for a in bridge.registry._assertions.values()
           if a.component_position is not None}
    assert not any(link.assertion_id in ids for link in bridge.proof_links)
    assert len(bridge.proof_links) == 1
    assert bridge.proof_links[0].step.rule is ProofRule.GIVEN
