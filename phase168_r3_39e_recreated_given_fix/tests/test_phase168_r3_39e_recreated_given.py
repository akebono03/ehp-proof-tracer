from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from proof import ProofRule


def test_web_proof_tree_does_not_recreate_concrete_toda51_given():
    context = []
    result = search_group_from_registered_goal(n=2, k=1, context_sink=context.append)
    assert result.status is ProofSearchStatus.COMPLETE
    assert len(context) == 1
    forbidden = {f'shared:1:adopted:assertion:{i}' for i in (1, 2, 4, 6)}
    cited_direct = {
        link.assertion_id for link in context[0].proof_links
        if link.step is not None and link.step.rule is ProofRule.GIVEN
    }
    assert forbidden.isdisjoint(cited_direct), sorted(forbidden.intersection(cited_direct))
    model = build_proof_narrative_model(
        result, registry=context[0].registry, proof_links=context[0].proof_links
    )
    bodies = tuple(body for cite in model.citations if cite.reference.locator == '(5.1)'
                   for body in cite.statement_bodies)
    assert bodies, 'Toda (5.1) reference bodies missing'
    assert any('\\pi_' in body for body in bodies), bodies
    assert not any('\\pi_2^1=0' in body for body in bodies), bodies


def test_other_two_goals_remain_complete():
    for n, k in ((3, 1), (4, 1)):
        result = search_group_from_registered_goal(n=n, k=k)
        assert result.status is ProofSearchStatus.COMPLETE, (n, k, result.status)
