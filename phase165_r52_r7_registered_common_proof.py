"""Phase 165 R52-R7: generic registered-proof dispatch and ancestry adapter.

The initial provider is the R38 typed pi3^2 proof. The dispatcher has no
(n, k) special cases and never trusts a repository conclusion as evidence.
Additional typed-proof providers can be added without changing dispatch logic.
"""
from __future__ import annotations

from dataclasses import replace

from proof import ProofRule
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance






def build_registered_common_replay(
    *, group_result: object, max_depth: int, mode: str,
):
    """Reconstruct a matched typed Goal now and send its proof to one renderer.

    A calculation result may propose the goal, but it is never a ProofStep.
    Neither a completed historical proof tree nor an unsupported claim is used.
    """
    from phase165_goal_only_search import GoalSearchIncompleteError

    if type(max_depth) is not int or max_depth < 0:
        raise ValueError("max_depth must be a nonnegative integer")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")
    from phase165_r52_r9_shared_math import search_shared_group_goal
    from phase165_goal_only_search import GoalSearchIncompleteError
    generated = search_shared_group_goal(
        n=group_result.target.sphere_dimension,
        k=(group_result.target.group_dimension - group_result.target.sphere_dimension),
        group_structure=group_result.group_structure,
    )
    from phase165_r52_partial_proof import ProofSearchStatus
    if generated.status is not ProofSearchStatus.COMPLETE:
        raise GoalSearchIncompleteError(
            "; ".join(generated.diagnostics) or "typed proof is incomplete"
        )
    root = next(
        (step for step in generated.proven_steps
         if step.conclusion == generated.conclusion), None
    )
    if root is None or root.rule not in (ProofRule.GIVEN, ProofRule.INFERENCE):
        raise GoalSearchIncompleteError("completed proof is not a typed proof step")
    group = group_result.target
    key = f"phase165:registered:pi{group.group_dimension}_{group.sphere_dimension}"
    source_entry = replace(
        group_result.source_entry,
        key=key, step=root, phase="165",
        theorem="Toda (5.1); Proposition 4.2; Proposition 5.1",
    )
    adapted = replace(group_result, source_entry=source_entry, proof_step=root)
    if mode == "narrative":
        provenance = extract_toda_recursive_proof_provenance(adapted)
        full_depth = max(node.shortest_depth for node in provenance.nodes)
        depth = max(max_depth, full_depth)
    else:
        depth = max_depth
    return build_toda_group_result_proof_replay(adapted, max_depth=depth)
