"""Read-only audit: render the newly reconstructed pi_5^3 ProofStep tree.

This module does not add mathematical premises or narrative substitutions.
"""

from dataclasses import dataclass

from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup
from phase162_pi5_3_backward_selection import (
    _canonical_goals,
    reconstruct_phase162_pi5_3_group_goal,
)
from proof import ProofStep
from proof_repository import ProofRepositoryEntry
from toda_group_proof_narrative_renderer import (
    render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
    TodaGroupProofPresentation,
    build_toda_group_proof_presentation,
)
from toda_group_result import TodaGroupResult
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


@dataclass(frozen=True)
class Pi53RendererAuditResult:
    final_step: ProofStep
    presentation: TodaGroupProofPresentation
    markdown: str


def render_phase162_pi5_3_reconstructed_proof(
    pi4_2_step: ProofStep,
    eta_definition_steps: tuple[ProofStep, ...],
    ehp_leaf_steps: tuple[ProofStep, ...],
) -> Pi53RendererAuditResult:
    """Reuse existing proof reconstruction and the public generic narrative path."""
    _, goal, _ = _canonical_goals()
    reconstruction = reconstruct_phase162_pi5_3_group_goal(
        goal, pi4_2_step, eta_definition_steps, ehp_leaf_steps
    )
    root = reconstruction.final_step
    if root.conclusion != goal or not isinstance(goal.rhs, FiniteCyclicGroup):
        raise ValueError("Reconstruction did not prove the requested pi_5^3 goal")
    entry = ProofRepositoryEntry(
        key="phase162-pi5-3-renderer-audit", step=root, phase="162"
    )
    group_result = TodaGroupResult(
        target=TodaPrimaryGroup(group_dimension=5, sphere_dimension=3),
        group_structure=goal.rhs,
        generators=(goal.rhs.generator,),
        generator_orders=(goal.rhs.order,),
        source_entry=entry,
        proof_step=root,
    )
    replay = build_toda_group_result_proof_replay(group_result, max_depth=40)
    presentation = build_toda_group_proof_presentation(replay)
    if presentation.root_step is not root:
        raise ValueError("Presentation replaced the reconstructed root")
    markdown = render_toda_group_proof_narrative_markdown(presentation)
    if not isinstance(markdown, str) or not markdown.strip():
        raise ValueError("Existing renderer returned empty Markdown")
    return Pi53RendererAuditResult(
        final_step=root, presentation=presentation, markdown=markdown
    )
