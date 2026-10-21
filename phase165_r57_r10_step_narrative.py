"""Shared typed-proof Narrative used when a legacy transport display would misstate ancestry.

This is an internal presentation helper; the one public entry remains
render_toda_group_proof_narrative_markdown. No theorem or premise is invented.
"""
from __future__ import annotations

from proof import ProofRule, ProofStep


def ordered_proof_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    """Return deduplicated ancestors before dependents, including the root."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be ProofStep")
    seen: set[int] = set()
    active: set[int] = set()
    ordered: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("every proof premise must be ProofStep")
        key = id(step)
        if key in active:
            raise ValueError("cyclic ProofStep ancestry")
        if key in seen:
            return
        active.add(key)
        for premise in step.premises:
            visit(premise)
        active.remove(key)
        seen.add(key)
        ordered.append(step)

    visit(root)
    return tuple(ordered)


def has_transport_proof_ancestry(root: ProofStep) -> bool:
    """Inspect proved inferences, never infer transport from a group number."""
    return any(
        step.rule is ProofRule.INFERENCE
        and (
            "transport" in str(getattr(step.inference_rule, "name", "")).lower()
            or "4.5" in str(getattr(step.inference_rule, "name", ""))
        )
        for step in ordered_proof_ancestry(root)
    )
