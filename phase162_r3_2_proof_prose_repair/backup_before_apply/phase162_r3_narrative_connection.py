"""Phase 162 R3: render the validated group-root proof, not map-property headings.

The existing public renderer remains unchanged. Reference lines can be carried
across verbatim from its output; the proof body is derived from the R2 graph.
"""

from dataclasses import dataclass

from expression import Composition, HomotopyElement, Suspension
from homotopy_groups import FiniteCyclicGroup, TodaPrimaryGroup, TodaSuspensionIsomorphismStatement
from phase162_r2_existing_proof_connection import ExistingProofConnectionResult
from proof import ProofRule, ProofStep, Relation, RelationType
from toda_rules import (
    TodaDeltaInjectiveStatement,
    TodaDeltaZeroStatement,
    TodaHopfInvariantSurjectiveStatement,
    TodaHopfInvariantZeroStatement,
    TodaSuspensionInjectiveStatement,
    TodaSuspensionSurjectiveStatement,
)


@dataclass(frozen=True)
class Phase162R3Narrative:
    markdown: str
    root_step: ProofStep
    ordered_steps: tuple[ProofStep, ...]


def _element_latex(element: object) -> str:
    if isinstance(element, HomotopyElement):
        gen = element.generator
        if gen is None or gen.index is None or not isinstance(gen.index, int):
            raise ValueError("Unsupported generator expression")
        decoration = gen.decoration or ""
        return f"{gen.family}_{{{gen.index}}}{decoration}"
    if isinstance(element, Composition):
        left = _element_latex(element.left)
        right = _element_latex(element.right)
        if element.left == element.right:
            return left + "^2"
        return left + r"\circ " + right
    if isinstance(element, Suspension):
        return "E(" + _element_latex(element.expression) + ")"
    raise ValueError(f"Unsupported element expression: {type(element).__name__}")


def _group_latex(group: TodaPrimaryGroup) -> str:
    if not isinstance(group, TodaPrimaryGroup):
        raise TypeError("Expected TodaPrimaryGroup")
    if not isinstance(group.group_dimension, int) or not isinstance(group.sphere_dimension, int):
        raise ValueError("Only concrete group dimensions are supported in R3")
    return rf"\pi_{{{group.group_dimension}}}^{{{group.sphere_dimension}}}"


def _structure_latex(statement: Relation) -> str:
    if not isinstance(statement, Relation) or statement.relation_type is not RelationType.EQUALITY:
        raise ValueError("Expected equality statement")
    if not isinstance(statement.rhs, FiniteCyclicGroup):
        raise ValueError("Expected finite cyclic structure")
    return (
        _group_latex(statement.lhs)
        + rf"=\mathbb{{Z}}/{statement.rhs.order}\{{"
        + _element_latex(statement.rhs.generator)
        + r"\}"
    )


def _ordered_ancestry(root: ProofStep) -> tuple[ProofStep, ...]:
    visited = set()
    active = set()
    result = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise ValueError("Unrecognized proof ancestry")
        identity = id(step)
        if identity in active:
            raise ValueError("Cyclic proof ancestry")
        if identity in visited:
            return
        active.add(identity)
        for premise in step.premises:
            visit(premise)
        active.remove(identity)
        visited.add(identity)
        result.append(step)

    visit(root)
    return tuple(result)


def _reference_section(existing_public_markdown: str | None) -> str:
    if existing_public_markdown is None:
        return ""
    if not isinstance(existing_public_markdown, str):
        raise TypeError("existing_public_markdown must be str or None")
    lines = existing_public_markdown.splitlines()
    try:
        start = next(i for i, line in enumerate(lines) if line.strip() == "## 使用する結果")
    except StopIteration:
        return ""
    end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")), len(lines))
    section = "\n".join(lines[start:end]).strip()
    return section


def render_phase162_r3_narrative(
    connection: ExistingProofConnectionResult,
    existing_public_markdown: str | None = None,
) -> Phase162R3Narrative:
    """Produce group-root text only after checking the expected dependency graph."""
    if not isinstance(connection, ExistingProofConnectionResult):
        raise TypeError("Expected validated R2 proof connection")
    root = connection.reconstruction.final_step
    if root.rule is not ProofRule.INFERENCE or root.conclusion != connection.reconstruction.goal:
        raise ValueError("Final goal must be a derived group-structure conclusion")
    if len(root.premises) != 3:
        raise ValueError("Group transport requires three premises")
    iso, source, image = root.premises
    if source is not connection.source_structure_step or image is not connection.generator_image_step:
        raise ValueError("Group structure premises differ from validated R2 connection")
    if not isinstance(iso.conclusion, TodaSuspensionIsomorphismStatement):
        raise ValueError("Expected suspension isomorphism premise")
    if root.inference_rule is None or root.inference_rule.name != "phase162_group_structure_transport":
        raise ValueError("Root was not derived by the group transport rule")
    ancestors = _ordered_ancestry(root)
    names = tuple(type(step.conclusion) for step in ancestors if step.rule is ProofRule.INFERENCE)
    expected = (
        TodaHopfInvariantSurjectiveStatement,
        TodaDeltaZeroStatement,
        TodaSuspensionInjectiveStatement,
        TodaDeltaInjectiveStatement,
        TodaHopfInvariantZeroStatement,
        TodaSuspensionSurjectiveStatement,
    )
    if any(not any(issubclass(t, target) for t in names) for target in expected):
        raise ValueError("Incomplete EHP reasoning ancestry")
    if iso.conclusion.map.source_group != source.conclusion.lhs:
        raise ValueError("Source group differs from isomorphism domain")
    if iso.conclusion.map.target_group != root.conclusion.lhs:
        raise ValueError("Target group differs from isomorphism codomain")
    if not isinstance(image.conclusion, Relation) or image.conclusion.relation_type is not RelationType.EQUALITY:
        raise ValueError("Generator image premise must be an equality")
    if image.conclusion.lhs != Suspension(source.conclusion.rhs.generator):
        raise ValueError("Generator image does not suspend source generator")
    if image.conclusion.rhs != root.conclusion.rhs.generator:
        raise ValueError("Generator image does not equal target generator")
    m = iso.conclusion.map
    source_group = _group_latex(m.source_group)
    target_group = _group_latex(m.target_group)
    target = _structure_latex(root.conclusion)
    source_eq = _structure_latex(source.conclusion)
    source_gen = _element_latex(source.conclusion.rhs.generator)
    target_gen = _element_latex(image.conclusion.rhs)
    left_h = next(s for s in ancestors if isinstance(s.conclusion, TodaHopfInvariantSurjectiveStatement))
    right_delta = next(s for s in ancestors if isinstance(s.conclusion, TodaDeltaInjectiveStatement))
    if left_h not in ancestors or right_delta not in ancestors:
        raise ValueError("Missing EHP input")
    heading = "# Group proof narrative\n\n## 証明対象\n\n$$\n" + target + "\n$$\n"
    refs = _reference_section(existing_public_markdown)
    if refs:
        heading += "\n" + refs + "\n"
    proof = (
        "\n---\n\n## 証明\n\n"
        "EHP 完全列を考える。既存の証明規則から、左側の Hopf 写像 $H$ は全射であり、"
        "右側の $\\Delta$ は単射である。したがって完全性により、"
        "$\\ker E=\\operatorname{im}\\Delta=0$ かつ "
        "$\\operatorname{im}E=\\ker H=" + target_group + "$ となる。"
        "よって\n\n$$\nE:" + source_group + r"\xrightarrow{\cong}" + target_group + "\n$$\n\n"
        "また、既存の群構造の証明から\n\n$$\n" + source_eq + "\n$$\n\n"
        "を得る。さらに $\\eta$-family の定義から\n\n$$\nE(" + source_gen + ")=" + target_gen + "\n$$\n\n"
        "が従う。以上より、群構造移送規則を適用して\n\n$$\n"
        + target + "\n$$\n\nを得る。 $\\square$\n"
    )
    return Phase162R3Narrative(markdown=heading + proof, root_step=root, ordered_steps=ancestors)


def render_phase162_r3_with_public_references(
    connection: ExistingProofConnectionResult,
    presentation: object,
) -> Phase162R3Narrative:
    """Reuse existing Reference layout while rendering a graph-derived proof body.

    Explicit integration entrypoint: caller retains control over which proof
    presentation belongs to the group and when this phase is enabled.
    """
    from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown

    existing_markdown = render_toda_group_proof_narrative_markdown(presentation)
    return render_phase162_r3_narrative(connection, existing_markdown)
