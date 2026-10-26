"""Phase 169 R3Y: source-bound codomain proof without dropping other valid routes."""
from __future__ import annotations

import pytest

from homotopy_groups import TodaHopfInvariantMap, TodaPrimaryGroup
from phase165_r14_r5_ehp_connection import expand_cited_ehp_terminal_goal
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved, SourceBoundGoal, reconstruct_registered_goal,
)
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from proof import ProofRule
from toda_rules import TodaHopfInvariantSurjectiveStatement


@pytest.fixture(scope="module")
def scope():
    bridge = build_shared_typed_bridge()
    target, = registered_group_goal_candidates(bridge, n=3, k=2)
    contexts = []
    result = search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    assert len(contexts) == 1
    ctx = contexts[0]
    citing = resolve_specialized_goal_citing_id(bridge, target)
    provider = shared_expansion_provider(ctx, proof_target=target)
    hopf = TodaHopfInvariantSurjectiveStatement(
        TodaHopfInvariantMap(TodaPrimaryGroup(6, 3), TodaPrimaryGroup(6, 5)),
    )
    sources = tuple(link.step.conclusion for link in ctx.proof_links
                    if link.step is not None and link.step.rule is ProofRule.GIVEN)
    return bridge, target, ctx, citing, provider, result, hopf, sources


def test_r3y_hopf_full_proof_has_derived_source_bound_codomain(scope):
    _, _, ctx, citing, provider, result, hopf, sources = scope
    assert result.status is ProofSearchStatus.COMPLETE
    option, = expand_cited_ehp_terminal_goal(hopf, sources)
    assert isinstance(option.subgoals[-1], SourceBoundGoal)
    step = reconstruct_registered_goal(hopf, ctx, citing, provider,
                                       lookup_mode="typed_reference_publication")
    assert step.rule is ProofRule.INFERENCE
    assert len(step.premises) == 3
    relation_step = step.premises[-1]
    assert relation_step.rule is ProofRule.INFERENCE
    assert relation_step.conclusion.lhs == hopf.map.target_group
    assert relation_step.premises[0].rule is ProofRule.GIVEN
    assert relation_step.premises[0].inference_rule.literature_reference.locator == "Proposition 5.1"


def test_r3y_no_source_no_hopf_inference(scope):
    _, _, _, _, _, _, hopf, sources = scope
    option, = expand_cited_ehp_terminal_goal(hopf, sources)
    source = option.subgoals[-1].source
    without = tuple(x for x in sources if x != source)
    assert expand_cited_ehp_terminal_goal(hopf, without) == ()


def test_r3y_source_bound_goal_is_fail_closed(scope):
    _, _, ctx, citing, provider, _, hopf, sources = scope
    option, = expand_cited_ehp_terminal_goal(hopf, sources)
    bound = option.subgoals[-1]
    proof = reconstruct_registered_goal(bound, ctx, citing, provider,
                                        lookup_mode="typed_reference_publication")
    assert proof.rule is ProofRule.INFERENCE
    assert proof.conclusion == bound.conclusion
    assert proof.premises[0].conclusion == bound.source
    with pytest.raises(RegisteredGoalUnresolved):
        reconstruct_registered_goal(
            SourceBoundGoal(bound.conclusion, "not a cited relation"),
            ctx, citing, provider,
            lookup_mode="typed_reference_publication",
        )


def test_r3y_unscoped_goal_retains_independent_proofs(scope):
    _, _, ctx, citing, provider, _, hopf, sources = scope
    option, = expand_cited_ehp_terminal_goal(hopf, sources)
    codomain = option.subgoals[-1].conclusion
    with pytest.raises(RegisteredGoalUnresolved, match="found 2"):
        reconstruct_registered_goal(codomain, ctx, citing, provider,
                                    lookup_mode="typed_reference_publication")
