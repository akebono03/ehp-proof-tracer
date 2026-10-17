"""Targeted regression: a source-adopted fourth claim is not self-proof."""
from phase165_prop51_claim_order import ordered_prop51_items, pi4_3_goal
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference
from phase165_r52_r12_component_bridge import expand_cited_given_components
from proof import ProofRule


def test_prop51_five_claims_in_order():
    bridge = build_adopted_prop51_reference()
    parent = bridge.registry.assertion('toda:adopted:prop5.1:finite_dimensional')
    items = ordered_prop51_items(parent.content)
    assert tuple(i.position for i in items) == (1, 2, 3, 4, 5)
    assert all(i.role == 'LITERATURE' for i in items)
    assert items[3].component_key == 'pi4_3_group_relation'
    assert items[3].statement == pi4_3_goal()


def test_prop51_fourth_claim_is_indexed_but_not_given():
    bridge = build_adopted_prop51_reference()
    claim = bridge.registry.assertion('toda:adopted:prop5.1:pi4_3')
    assert claim.component_position == 4
    assert claim.content == pi4_3_goal()
    assert not any(link.assertion_id == claim.assertion_id for link in bridge.proof_links)
    expanded = expand_cited_given_components(bridge)
    assert not any(link.step.rule is ProofRule.GIVEN and link.step.conclusion == claim.content for link in expanded.proof_links)


def test_prop51_existing_four_given_components_remain_available():
    bridge = expand_cited_given_components(build_adopted_prop51_reference())
    for name in ('pi3_2_group_relation','eta2_hopf_relation','delta_iota5_relation','higher_eta_group_relation'):
        assert any(link.assertion_id.endswith(':component:'+name) for link in bridge.proof_links)
