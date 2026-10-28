"""Focused regression: new stable definition plus existing root and trust gate."""
from __future__ import annotations

from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase168_r3_41p13_trust_boundary import verify_proof_tree_for_narrative


def test_r10eq_pi44_30_arbitrary_stable_element_transport():
    contexts = []
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(
        n=30, k=14, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )


def test_r10eq_pi41_30_reviewed_cited_stable_proof_still_complete():
    contexts = []
    bridge = build_shared_typed_bridge()
    result = search_group_from_registered_goal(
        n=30, k=11, bridge=bridge, context_sink=contexts.append,
    )
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.open_goals == ()
    assert len(contexts) == 1
    citing = resolve_specialized_goal_citing_id(bridge, result.conclusion)
    verify_proof_tree_for_narrative(
        result, contexts[0], citing_assertion_id=citing,
        derived_target_without_citing_id=citing is None,
    )
