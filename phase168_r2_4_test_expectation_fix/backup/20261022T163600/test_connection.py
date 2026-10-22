from dataclasses import replace

from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule


def test_pi54_source_is_unique_and_precedes_pi43():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=4, k=1)
    assert len(goals) == 1
    citing = resolve_specialized_goal_citing_id(bridge, goals[0])
    assert citing == 'shared:2:toda:adopted:prop5.1:higher_eta_group_relation'
    screened = screen_shared_proof_context(bridge, goal=goals[0], citing_assertion_id=citing,
                                           explicit_publication_target=True)
    ids = [link.assertion_id for link in screened.proof_links]
    assert 'shared:2:toda:adopted:prop5.1:pi4_3' in ids
    assert citing not in ids
    assert all(link.step.rule is ProofRule.GIVEN for link in screened.proof_links)


def test_pi43_is_not_assigned_pi54_citing_id():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=1)
    assert len(goals) == 1
    assert resolve_specialized_goal_citing_id(bridge, goals[0]) is None


def test_pi32_is_not_assigned_pi54_citing_id():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=2, k=1)
    assert len(goals) == 1
    assert resolve_specialized_goal_citing_id(bridge, goals[0]) is None
