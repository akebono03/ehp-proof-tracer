"""R12-R14: close an EHP suspension-kernel goal through shared backward search.

No new mathematical axioms, no synthetic GIVEN, and no group-specific rule.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase163_r4_registry_bridge import RegistryBridgeResult
from phase165_r12_r11_prop42_unified import prefer_universal_prop42_derivation
from phase165_r12_r12_ehp_consequences import proof_has_general_prop42_ancestor
from phase165_r12_r13_kernel_image import SuspensionKernelFreeCyclicStatement
from phase165_r3_recursive_search import (
    RegisteredGoalUnresolved,
    reconstruct_registered_goal,
)
from phase165_r52_r9_shared_math import shared_expansion_provider
from phase165_r52_r16_web_citation_gate import screen_shared_proof_context
from proof import ProofRule, ProofStep


@dataclass(frozen=True)
class KernelClosureResult:
    """Proof (only if verified by recursive search) or a transparent blocker."""
    goal: SuspensionKernelFreeCyclicStatement
    proof: ProofStep | None
    status: str
    blocker: str | None


def prove_kernel_in_screened_context(
    goal: SuspensionKernelFreeCyclicStatement,
    bridge: RegistryBridgeResult,
    *,
    citing_assertion_id: str,
    proof_target: object,
) -> KernelClosureResult:
    """Run the actual rule matcher, preserving R11-R13 source and step ancestry.

    The caller provides the intended proof target, so source screening never
    silently substitutes the kernel goal for the citing group assertion.
    """
    if not isinstance(goal, SuspensionKernelFreeCyclicStatement):
        raise TypeError("typed suspension kernel goal required")
    if not isinstance(bridge, RegistryBridgeResult):
        raise TypeError("registry bridge required")
    screened = screen_shared_proof_context(
        bridge,
        goal=proof_target,
        citing_assertion_id=citing_assertion_id,
    )
    screened = prefer_universal_prop42_derivation(screened)
    expansion = shared_expansion_provider(screened, proof_target=proof_target)
    try:
        proof = reconstruct_registered_goal(
            goal,
            screened,
            citing_assertion_id=citing_assertion_id,
            expansion_provider=expansion,
            lookup_mode="typed_reference",
        )
    except RegisteredGoalUnresolved as exc:
        return KernelClosureResult(goal, None, "UNRESOLVED", str(exc))
    if proof.conclusion != goal or proof.rule is not ProofRule.INFERENCE:
        return KernelClosureResult(goal, None, "INVALID_ROOT", "non-inference kernel root")
    if not proof_has_general_prop42_ancestor(proof):
        return KernelClosureResult(goal, None, "MISSING_PROVENANCE", "no general Prop. 4.2 ancestor")
    return KernelClosureResult(goal, proof, "CERTIFIED", None)


def summarize_proof_ancestry(step: ProofStep) -> dict[str, object]:
    """Count actual proof nodes, not search candidates or adopted-source labels."""
    visited: set[int] = set()
    counts = {"given": 0, "inference": 0, "other": 0}
    def walk(node: ProofStep) -> None:
        if id(node) in visited:
            return
        visited.add(id(node))
        if node.rule is ProofRule.GIVEN:
            counts["given"] += 1
        elif node.rule is ProofRule.INFERENCE:
            counts["inference"] += 1
        else:
            counts["other"] += 1
        for parent in node.premises:
            walk(parent)
    walk(step)
    return {"node_count": len(visited), **counts,
            "has_general_prop42_ancestor": proof_has_general_prop42_ancestor(step)}
