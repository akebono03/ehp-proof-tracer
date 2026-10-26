"""Phase 169 R3I2: closure after cited terminal premise construction."""
from homotopy_groups import TodaPrimaryGroup
from phase165_r3_recursive_search import reconstruct_registered_goal
from phase165_r52_partial_proof import ProofSearchStatus
from phase165_r52_r9_shared_math import build_shared_typed_bridge, shared_expansion_provider
from phase165_r55_nk_only_goal import registered_group_goal_candidates, search_group_from_registered_goal
from phase166_r3t_goal_source_binding.goal_source import resolve_specialized_goal_citing_id
from phase169_r3i2_import_repair.audit import validate_completed_proof_tree


def test_r3i1_pi53_complete_only_with_exact_database_goal():
    bridge = build_shared_typed_bridge()
    goals = registered_group_goal_candidates(bridge, n=3, k=2)
    assert len(goals) == 1
    result = search_group_from_registered_goal(n=3, k=2, bridge=bridge)
    assert result.status is ProofSearchStatus.COMPLETE
    assert result.conclusion == goals[0]
    assert result.target == TodaPrimaryGroup(5, 3)
    assert result.open_goals == ()
    assert any(step.conclusion == goals[0] for step in result.proven_steps)


def test_r3i1_completed_tree_has_only_prior_cited_givens_and_verified_inferences():
    bridge = build_shared_typed_bridge()
    goal, = registered_group_goal_candidates(bridge, n=3, k=2)
    citing = resolve_specialized_goal_citing_id(bridge, goal)
    assert citing == "shared:0:boundary:Proposition 5.3:pi5_3_group_relation"
    contexts = []
    search_group_from_registered_goal(n=3, k=2, bridge=bridge, context_sink=contexts.append)
    assert len(contexts) == 1
    screened = contexts[0]
    provider = shared_expansion_provider(screened, proof_target=goal)
    root = reconstruct_registered_goal(
        goal, screened, citing, provider, lookup_mode="typed_reference_publication",
    )
    closure = validate_completed_proof_tree(root, screened, citing)
    assert closure["all_givens_prior"]
    assert closure["all_inferences_replayed"]
    assert closure["given_count"] >= 2
    assert closure["inference_count"] >= 3
    assert len(closure["terminal_rule_names"]) == 2
