"""Phase 162 R2: a validated, map-goal proof presentation boundary.

This does not pretend that a map-property proof is a TodaGroupResult.
The established common ProofStep statement renderer remains the prose source.
"""

from dataclasses import dataclass
import re

from phase161_r7_premise_provenance_validation import (
    ValidatedBackwardReconstruction,
    validate_phase161_r7_provenance,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_literature_statement_boundary import (
    TodaLiteratureStatementClassification,
    classify_toda_literature_statement_step,
)
from toda_group_proof_narrative_references import (
    TodaGroupProofNarrativeReferenceEntry,
    extract_toda_group_proof_step_literature_reference,
    render_toda_group_proof_narrative_reference_entries_markdown,
)
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
    TodaProp42ExactnessStatement,
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


def build_validated_proof_reference_entries(
    presentation: ValidatedProofPresentation,
) -> tuple[TodaGroupProofNarrativeReferenceEntry, ...]:
    """Collect only classified fixed literature statements from verified ancestry.

    Group by literature locator; proof-internal uses never become references
    merely because their inference rules mention Toda's propositions.
    """
    if not isinstance(presentation, ValidatedProofPresentation):
        raise TypeError("presentation must be a ValidatedProofPresentation")
    references = []
    groups = []
    locator_to_index = {}
    for step in presentation.nodes:
        boundary = classify_toda_literature_statement_step(step)
        if (
            boundary is None
            or boundary.classification
            is not TodaLiteratureStatementClassification.FIXED_STATEMENT
        ):
            continue
        reference = extract_toda_group_proof_step_literature_reference(step)
        if reference is None:
            raise ValueError("Fixed literature statement has no reference")
        locator = boundary.reference_locator
        if reference.locator != locator:
            raise ValueError("Fixed literature locator mismatch")
        position = locator_to_index.get(locator)
        if position is None:
            position = len(references)
            locator_to_index[locator] = position
            references.append(reference)
            groups.append([])
        groups[position].append(step)
    return tuple(
        TodaGroupProofNarrativeReferenceEntry(
            number=index, reference=reference, proof_steps=tuple(steps),
        )
        for index, (reference, steps) in enumerate(zip(references, groups), 1)
    )


def _render_validated_reference_section(
    presentation: ValidatedProofPresentation,
) -> tuple[str, frozenset[int]]:
    entries = build_validated_proof_reference_entries(presentation)
    if not entries:
        return "", frozenset()
    statement_lines = {}
    referenced_ids = set()
    for entry in entries:
        lines = []
        seen = set()
        for step in entry.proof_steps:
            referenced_ids.add(id(step))
            statement = _render_validated_backward_step(step)
            if statement not in seen:
                seen.add(statement)
                lines.append(statement)
        statement_lines[entry.number] = tuple(lines)
    return (
        render_toda_group_proof_narrative_reference_entries_markdown(
            entries, statement_lines_by_reference_number=statement_lines,
        ).rstrip(),
        frozenset(referenced_ids),
    )


def _is_display_tautology(step: ProofStep, prose: str) -> bool:
    """Hide a visibly reflexive equality, without changing its ProofStep."""
    statement = step.conclusion
    if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
        return False
    normalized = prose.strip().rstrip(".。")
    match = re.fullmatch(r"\$([^$]+)\$", normalized)
    if match is None:
        return False
    parts = match.group(1).split(" = ")
    return len(parts) == 2 and parts[0].strip() == parts[1].strip()


def _validated_proof_body_lines(
    presentation: ValidatedProofPresentation,
    reference_step_ids: frozenset[int],
) -> tuple[str, ...]:
    """Suppress duplicate display without modifying validated proof ancestry.

    ProofStep identity and semantic equality continue to control reference
    attribution and mathematical inference. Text-based checks are used ONLY
    for redundant public presentation, never for proof validity.
    """
    seen_conclusions = []
    seen_rendered = set()
    reference_lines = set()
    for entry in build_validated_proof_reference_entries(presentation):
        for fixed_step in entry.proof_steps:
            reference_lines.add(_render_validated_backward_step(fixed_step).strip())
    lines = []
    for step in presentation.nodes:
        if step.rule is ProofRule.GIVEN or id(step) in reference_step_ids:
            continue
        statement = step.conclusion
        if (
            isinstance(statement, Relation)
            and statement.relation_type is RelationType.EQUALITY
            and statement.lhs == statement.rhs
        ):
            continue
        if any(statement == previous for previous in seen_conclusions):
            continue
        seen_conclusions.append(statement)
        prose = _render_validated_backward_step(step)
        normalized = prose.strip()
        if _is_display_tautology(step, prose):
            continue
        if normalized in seen_rendered or normalized in reference_lines:
            continue
        seen_rendered.add(normalized)
        if (
            any(
                isinstance(premise.conclusion, TodaProp42ExactnessStatement)
                for premise in step.premises
            )
            and isinstance(
                statement,
                (TodaSuspensionInjectiveStatement, TodaSuspensionSurjectiveStatement),
            )
        ):
            prose = "完全性より、" + prose
        lines.append(prose)
    return tuple(lines)


def render_validated_backward_proof_markdown(
    presentation: ValidatedProofPresentation,
) -> str:
    """Render the verified proof with classified references and concise prose."""
    if not isinstance(presentation, ValidatedProofPresentation):
        raise TypeError("presentation must be a ValidatedProofPresentation")
    if not presentation.nodes or presentation.nodes[-1] is not presentation.root_step:
        raise ValueError("Invalid presentation root ordering")

    reference_section, reference_step_ids = _render_validated_reference_section(
        presentation
    )
    lines = ["# Backward proof narrative", ""]
    if reference_section:
        lines.extend(("## 使用する結果", "", reference_section, "", "---", ""))
    lines.extend(("## 証明", ""))
    for prose in _validated_proof_body_lines(presentation, reference_step_ids):
        lines.extend((prose, ""))
    lines.extend(("□", ""))
    return "\n".join(lines)
