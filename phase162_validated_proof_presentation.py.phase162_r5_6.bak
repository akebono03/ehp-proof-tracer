"""Phase 162 R2: a validated, map-goal proof presentation boundary.

This does not pretend that a map-property proof is a TodaGroupResult.
The established common ProofStep statement renderer remains the prose source.
"""

from dataclasses import dataclass
import re

from expression import IteratedSuspension

from phase161_r7_premise_provenance_validation import (
    ValidatedBackwardReconstruction,
    validate_phase161_r7_provenance,
)
from proof import ProofRule, ProofStep, Relation, RelationType
from repository_element_presentation import render_repository_conclusion_latex
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
from toda_general_reference_schema import render_general_reference_statement_lines
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
    """Keep structural suspension expressions before normalizing prose.

    Generic prose is still the default for all other statement types.  A
    relation involving iterated suspension must retain its E-exponent, even
    when a generator-normalizing renderer would show equal normal forms.
    """
    conclusion = step.conclusion
    if (
        isinstance(conclusion, Relation)
        and conclusion.relation_type is RelationType.EQUALITY
        and (
            isinstance(conclusion.lhs, IteratedSuspension)
            or isinstance(conclusion.rhs, IteratedSuspension)
        )
    ):
        return "$" + render_repository_conclusion_latex(conclusion) + "$"

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
    """Render registered source statements without reattaching inferred ranges.

    The legacy renderer is retained for locators without a general schema.
    Referenced ProofStep identities are unchanged in either case.
    """
    entries = build_validated_proof_reference_entries(presentation)
    if not entries:
        return "", frozenset()

    referenced_ids = frozenset(
        id(step) for entry in entries for step in entry.proof_steps
    )
    blocks = []
    for entry in entries:
        locator = entry.reference.locator
        general_lines = render_general_reference_statement_lines(locator)
        if general_lines is not None:
            title = locator or entry.reference.label
            blocks.append("\n".join((
                f"**[R{entry.number}] {title}.**",
                *general_lines,
            )))
            continue

        rendered_lines = []
        seen = set()
        for step in entry.proof_steps:
            statement = _render_validated_backward_step(step)
            if statement not in seen:
                seen.add(statement)
                rendered_lines.append(statement)
        blocks.append(
            render_toda_group_proof_narrative_reference_entries_markdown(
                (entry,),
                statement_lines_by_reference_number={
                    entry.number: tuple(rendered_lines)
                },
            ).rstrip()
        )

    return "\n".join(blocks).rstrip(), referenced_ids


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



def _validated_reference_number_by_step_id(
    presentation: ValidatedProofPresentation,
) -> dict[int, int]:
    """Bind each fixed source ProofStep identity to its public reference number."""
    return {
        id(step): entry.number
        for entry in build_validated_proof_reference_entries(presentation)
        for step in entry.proof_steps
    }


def _direct_reference_markers(
    step: ProofStep,
    reference_number_by_id: dict[int, int],
) -> tuple[str, ...]:
    """Attribute only direct, identity-matched fixed literature premises."""
    numbers = sorted({
        reference_number_by_id[id(premise)]
        for premise in step.premises
        if id(premise) in reference_number_by_id
    })
    return tuple(f"[R{number}]" for number in numbers)


def _validated_proof_body_step_lines(
    presentation: ValidatedProofPresentation,
    reference_step_ids: frozenset[int],
) -> tuple[tuple[ProofStep, str], ...]:
    """Render visible proof steps while preserving their source identities."""
    reference_number_by_id = _validated_reference_number_by_step_id(presentation)
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
        markers = _direct_reference_markers(step, reference_number_by_id)
        if markers:
            prose = ", ".join(markers) + "より、" + prose
        lines.append((step, prose))
    return tuple(lines)


def _validated_proof_body_lines(
    presentation: ValidatedProofPresentation,
    reference_step_ids: frozenset[int],
) -> tuple[str, ...]:
    """Backward-compatible flat body, retaining all existing prose contracts."""
    return tuple(
        prose for _, prose in _validated_proof_body_step_lines(
            presentation, reference_step_ids
        )
    )


def _validated_proof_branch_ids(root: ProofStep) -> tuple[frozenset[int], frozenset[int]] | None:
    """Find the two proof ancestries from the actual root, not rendered text."""
    if len(root.premises) != 2:
        return None
    injective = next(
        (step for step in root.premises
         if isinstance(step.conclusion, TodaSuspensionInjectiveStatement)),
        None,
    )
    surjective = next(
        (step for step in root.premises
         if isinstance(step.conclusion, TodaSuspensionSurjectiveStatement)),
        None,
    )
    if injective is None or surjective is None:
        return None

    def ancestry_ids(start: ProofStep) -> frozenset[int]:
        visited = set()
        def visit(step: ProofStep) -> None:
            if id(step) in visited:
                return
            visited.add(id(step))
            for premise in step.premises:
                visit(premise)
        visit(start)
        return frozenset(visited)

    return ancestry_ids(injective), ancestry_ids(surjective)


def _composed_validated_proof_sections(
    presentation: ValidatedProofPresentation,
    reference_step_ids: frozenset[int],
) -> tuple[tuple[str, tuple[str, ...]], ...]:
    """Partition topologically ordered steps by proven branch ancestry.

    Shared prerequisites appear once in preparation. Branch-specific steps
    remain in their premise-before-conclusion order. Unknown goal shapes
    retain the original flat proof without fabricated sections.
    """
    records = _validated_proof_body_step_lines(presentation, reference_step_ids)
    branches = _validated_proof_branch_ids(presentation.root_step)
    if branches is None:
        return (("証明", tuple(prose for _, prose in records)),)
    injective_ids, surjective_ids = branches
    shared_ids = injective_ids & surjective_ids
    sections = {"準備": [], "単射性": [], "全射性": [], "結論": []}
    for step, prose in records:
        identifier = id(step)
        if step is presentation.root_step:
            sections["結論"].append(prose)
        elif identifier in shared_ids:
            sections["準備"].append(prose)
        elif identifier in injective_ids:
            sections["単射性"].append(prose)
        elif identifier in surjective_ids:
            sections["全射性"].append(prose)
        else:
            # A proof node outside both final branches must not be dropped.
            sections["準備"].append(prose)
    return tuple(
        (label, tuple(lines)) for label, lines in sections.items() if lines
    )


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
    for heading, prose_lines in _composed_validated_proof_sections(
        presentation, reference_step_ids
    ):
        if heading != "証明":
            lines.extend(("### " + heading, ""))
        for prose in prose_lines:
            lines.extend((prose, ""))
    lines.extend(("□", ""))
    return "\n".join(lines)
