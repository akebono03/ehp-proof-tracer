"""Phase 165 R52-R7: generic registered-proof dispatch and ancestry adapter.

The initial provider is the R38 typed pi3^2 proof. The dispatcher has no
(n, k) special cases and never trusts a repository conclusion as evidence.
Additional typed-proof providers can be added without changing dispatch logic.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Callable

from proof import ProofStep, ProofRule, Relation
from toda_group_result_proof_replay import build_toda_group_result_proof_replay
from toda_proof_dependency import extract_toda_recursive_proof_provenance


@dataclass(frozen=True)
class RegisteredProofProvider:
    name: str
    goal: object
    reconstruct: Callable[[], tuple[object, ProofStep]]
    theorem: str
    phase: str = "165"


def registered_proof_providers() -> tuple[RegisteredProofProvider, ...]:
    """Explicitly register available typed proofs, not stored completed trees.

    This inventory is a transitional dependency until the unified registry
    supplies typed goal/expansion registrations for additional dimensions.
    """
    from phase165_r14_r34_backward_search import pi32_goal
    from phase165_r14_r38_direct_registry import reconstruct_registered_pi32

    tex = Path(__file__).resolve().with_name("phase165_r14_r39_toda51.tex")
    return (RegisteredProofProvider(
        name="phase165:registered:pi3_2",
        goal=pi32_goal(),
        reconstruct=lambda: reconstruct_registered_pi32(tex),
        theorem="Toda (5.1); Proposition 4.2; Proposition 5.1",
    ),)


def build_registered_common_replay(
    *, group_result: object, max_depth: int, mode: str,
    providers: tuple[RegisteredProofProvider, ...] | None = None,
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
    if providers is None:
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
        if root is None or root.rule is not ProofRule.INFERENCE:
            raise GoalSearchIncompleteError("completed proof is not an inference")
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
    if not isinstance(providers, tuple) or not all(
        isinstance(candidate, RegisteredProofProvider) for candidate in providers
    ):
        raise TypeError("providers must contain RegisteredProofProvider objects")
    goal = Relation(lhs=group_result.target, rhs=group_result.group_structure)
    matches = tuple(provider for provider in providers
                    if type(provider.goal) is type(goal) and provider.goal == goal)
    if len(matches) != 1:
        raise GoalSearchIncompleteError(
            f"expected one configured typed proof for {goal!r}, found {len(matches)}"
        )
    provider = matches[0]
    bridge, root = provider.reconstruct()
    if not isinstance(root, ProofStep) or root.rule is not ProofRule.INFERENCE:
        raise ValueError("registered search did not derive an inference ProofStep")
    if type(root.conclusion) is not type(goal) or root.conclusion != goal:
        raise ValueError("registered proof does not establish the requested group")
    if not bridge.proof_links:
        raise ValueError("registered proof has no typed source links")
    source_entry = replace(
        group_result.source_entry,
        key=provider.name, step=root, phase=provider.phase,
        theorem=provider.theorem,
    )
    adapted = replace(group_result, source_entry=source_entry, proof_step=root)
    if mode == "narrative":
        provenance = extract_toda_recursive_proof_provenance(adapted)
        full_depth = max(node.shortest_depth for node in provenance.nodes)
        depth = max(max_depth, full_depth)
    else:
        depth = max_depth
    return build_toda_group_result_proof_replay(adapted, max_depth=depth)
