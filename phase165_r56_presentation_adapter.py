"""Adapt completed canonical searches to the established public Toda narrative.

All mathematical evidence comes from the typed search's ProofStep ancestry.
The existing public renderer owns headings, citations and mathematical prose.
"""
from __future__ import annotations

from homotopy_groups import DirectSumGroup, FiniteCyclicGroup, FreeCyclicGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from proof import ProofRule
from proof_repository import ProofRepositoryEntry
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_complete_toda_group_result_proof_replay
from toda_group_proof_presentation import build_toda_group_proof_presentation
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def render_completed_shared_narrative(result: PartialProofResult) -> str:
    """Render a completed typed proof through the existing shared Narrative renderer."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is not ProofSearchStatus.COMPLETE or result.conclusion is None:
        raise ValueError("a complete search is required")
    conclusion = result.conclusion
    if getattr(conclusion, "lhs", None) != result.target:
        raise ValueError("completed target does not match conclusion")
    structure = getattr(conclusion, "rhs", None)
    if not isinstance(structure, (FreeCyclicGroup, FiniteCyclicGroup, DirectSumGroup)):
        raise ValueError("unsupported group structure in completed goal")
    roots = [step for step in result.proven_steps if step.conclusion == conclusion]
    if len(roots) != 1 or roots[0].rule is not ProofRule.INFERENCE:
        raise ValueError("completed proof must contain exactly one derived root")
    root = roots[0]
    if isinstance(structure, FreeCyclicGroup):
        generators = (structure.generator,)
        orders = (None,)
    elif isinstance(structure, FiniteCyclicGroup):
        generators = (structure.generator,)
        orders = (structure.order,)
    else:
        raise ValueError("direct-sum presentation requires typed generators")
    entry = ProofRepositoryEntry(key="phase165:typed:completed", step=root, phase="165")
    group_result = TodaGroupResult(
        target=result.target,
        group_structure=structure,
        generators=generators,
        generator_orders=orders,
        source_entry=entry,
        proof_step=root,
    )
    replay = build_complete_toda_group_result_proof_replay(group_result)
    presentation = build_toda_group_proof_presentation(replay)
    return render_toda_group_proof_narrative_markdown(presentation)
