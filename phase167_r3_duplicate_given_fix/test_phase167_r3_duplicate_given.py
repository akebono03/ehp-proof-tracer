from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule


def test_phase167_r3_publication_context_deduplicates_equivalent_assertions():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=1)
    assert len(goals) == 1
    citing_id = resolve_specialized_goal_citing_id(bridge, goals[0])
    assert citing_id == 'shared:2:toda:adopted:prop5.1:pi4_3'
    screened = screen_shared_proof_context(bridge, goal=goals[0], citing_assertion_id=citing_id,
                                            explicit_publication_target=True)
    for i, first in enumerate(screened.proof_links):
        first_assertion = bridge.registry.assertion(first.assertion_id)
        first_ref = bridge.registry.reference(first_assertion.reference_id)
        for second in screened.proof_links[i+1:]:
            second_assertion = bridge.registry.assertion(second.assertion_id)
            second_ref = bridge.registry.reference(second_assertion.reference_id)
            assert not (
                first.step.conclusion == second.step.conclusion
                and first_ref.publication_position == second_ref.publication_position
                and first_assertion.component_position == second_assertion.component_position
            )
    assert all(link.step.conclusion != goals[0] for link in screened.proof_links)


def test_phase167_r3_both_completed_proofs_after_dedup():
    for n in (2, 3):
        result = search_group_from_registered_goal(n=n, k=1)
        assert result.status is ProofSearchStatus.COMPLETE, (n, result.diagnostics, result.open_goals)
        assert not any(step.rule is ProofRule.GIVEN and step.conclusion == result.conclusion
                       for step in result.proven_steps)
