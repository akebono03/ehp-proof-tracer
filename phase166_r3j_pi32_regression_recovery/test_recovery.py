"""Focused regression test: the R3-J ordering additions cannot break pi3^2 Web search."""
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_r13_reference_registration import build_adopted_prop51_reference


def test_pi32_public_search_remains_complete():
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE, (
        result.status, result.diagnostics, result.open_goals
    )


def test_prop51_ordered_assertions_preserved():
    bridge = build_adopted_prop51_reference()
    positions = {
        a.assertion_id.rsplit(':', 1)[-1]: a.component_position
        for a in bridge.registry._assertions.values()
        if a.component_position is not None
    }
    assert positions == {
        'eta2_hopf_relation': 1,
        'pi3_2_group_relation': 2,
        'delta_iota5_relation': 3,
        'pi4_3': 4,
        'higher_eta_group_relation': 5,
    }
