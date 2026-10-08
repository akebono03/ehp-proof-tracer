"""Phase 162 R2: a validated, map-goal proof presentation boundary.

This does not pretend that a map-property proof is a TodaGroupResult.
The established common ProofStep statement renderer remains the prose source.
"""

from dataclasses import dataclass

from phase161_r7_premise_provenance_validation import (
    ValidatedBackwardReconstruction,
    validate_phase161_r7_provenance,
)
from proof import ProofRule, ProofStep
from toda_group_proof_generic_narrative_renderer import (
    _render_generic_narrative_step,
)
from toda_group_proof_narrative_renderer import (
    _render_group_proof_narrative_latex,
)
from toda_proof_dependency import TodaProofEdge
from toda_rules import (
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


@dataclass(frozen=True)
class ValidatedProofPresentation:
    root_step: ProofStep
    nodes: tuple[ProofStep, ...]
    edges: tuple[TodaProofEdge, ...]


def _ordered_premises(step: ProofStep) -> tuple[tuple[int, ProofStep], ...]:
    """Prefer injectivity before surjectivity when both establish one goal."""
    indexed = tuple(enumerate(step.premises))
    if len(indexed) != 2:
        return indexed
    statements = tuple(p.conclusion for _, p in indexed)
    if (
        any(isinstance(s, TodaSuspensionInjectiveStatement) for s in statements)
        and any(isinstance(s, TodaSuspensionSurjectiveStatement) for s in statements)
    ):
        return tuple(sorted(indexed, key=lambda item: (
            0 if isinstance(item[1].conclusion, TodaSuspensionInjectiveStatement)
            else 1,
            item[0],
        )))
    return indexed


def build_validated_backward_proof_presentation(
    validated: ValidatedBackwardReconstruction,
) -> ValidatedProofPresentation:
    if not isinstance(validated, ValidatedBackwardReconstruction):
        raise TypeError("validated must be a ValidatedBackwardReconstruction")
    root = validated.reconstruction.final_step
    if root.conclusion != validated.reconstruction.goal:
        raise ValueError("Reconstructed root does not prove the requested goal")

    # Revalidate *the same* concrete proof ancestry, including GIVEN identities.
    validate_phase161_r7_provenance(
        (root,), validated.provenance.trusted_roots_used
    )

    visited: set[int] = set()
    ordered: list[ProofStep] = []
    edges: list[TodaProofEdge] = []

    def visit(step: ProofStep) -> None:
        key = id(step)
        if key in visited:
            return
        visited.add(key)
        for premise_index, premise in _ordered_premises(step):
            edges.append(TodaProofEdge(
                parent_step=step,
                premise_step=premise,
                premise_index=premise_index,
            ))
            visit(premise)
        ordered.append(step)

    visit(root)
    return ValidatedProofPresentation(
        root_step=root,
        nodes=tuple(ordered),
        edges=tuple(edges),
    )


def _render_validated_backward_step(step: ProofStep) -> str:
    """Use existing statement prose, then existing mathematical LaTeX renderer."""
    prose = _render_generic_narrative_step(step)
    fallback = (
        step.inference_rule.name if step.inference_rule is not None else None
    )
    if prose and prose != fallback and prose != f"`{type(step.conclusion).__name__}`":
        return prose
    latex = _render_group_proof_narrative_latex(step)
    if latex:
        return "$" + latex + "$"
    raise ValueError(
        "Common renderers have no mathematical representation for "
        + type(step.conclusion).__name__
    )


def render_validated_backward_proof_markdown(
    presentation: ValidatedProofPresentation,
) -> str:
    """Render verified inference statements via existing common renderers."""
    if not isinstance(presentation, ValidatedProofPresentation):
        raise TypeError("presentation must be a ValidatedProofPresentation")
    if not presentation.nodes or presentation.nodes[-1] is not presentation.root_step:
        raise ValueError("Invalid presentation root ordering")

    lines = ["# Backward proof narrative", "", "## 証明", ""]
    for step in presentation.nodes:
        if step.rule is ProofRule.GIVEN:
            continue  # R3 owns reference presentation and GIVEN attribution.
        lines.extend((_render_validated_backward_step(step), ""))
    lines.extend(("□", ""))
    return "\n".join(lines)
