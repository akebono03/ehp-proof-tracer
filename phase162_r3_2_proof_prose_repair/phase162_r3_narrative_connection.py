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
        family_latex = {"η": r"\eta", "ι": r"\iota"}.get(gen.family, gen.family)
        return f"{family_latex}_{{{gen.index}}}{decoration}"
    if isinstance(element, Composition):
        left = _element_latex(element.left)
        right = _element_latex(element.right)
        left_generator = getattr(element.left, "generator", None)
        right_generator = getattr(element.right, "generator", None)
        if (
            left_generator is not None
            and right_generator is not None
            and left_generator.family == "η"
            and right_generator.family == "η"
            and isinstance(left_generator.index, int)
            and right_generator.index == left_generator.index + 1
            and not left_generator.decoration
            and not right_generator.decoration
        ):
            return left + "^{2}"
        if element.left == element.right:
            return left + "^{2}"
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


def _phase162_legacy_ehp_body(existing_public_markdown: str | None) -> str | None:
    """Reuse the fully validated R7 EHP prose, not an abbreviated substitute.

    Keep its reasoning and ASCII punctuation intact. Only the artificial
    section headings are dropped, because EHP is one part of a group proof.
    """
    if existing_public_markdown is None:
        return None
    if not isinstance(existing_public_markdown, str):
        raise TypeError("existing_public_markdown must be str or None")
    if "## 証明\n" not in existing_public_markdown:
        return None
    proof = existing_public_markdown.split("## 証明\n", 1)[1]
    if not all(label in proof for label in ("### 単射性", "### 全射性", "### 結論")):
        return None
    proof = proof.split("### 結論", 1)[0]
    proof = "\n".join(
        line for line in proof.splitlines()
        if line.strip() not in ("### 準備", "### 単射性", "### 全射性")
    )
    if "EHP 完全列" not in proof or "Proposition 5.1" not in proof:
        raise ValueError("Expected validated EHP proof details in legacy narrative")
    return proof.strip()

def render_phase162_r3_narrative(
    connection: ExistingProofConnectionResult,
    existing_public_markdown: str | None = None,
) -> Phase162R3Narrative:
    """Render the group-root proof with the full verified EHP argument.

    The proof ends at the root InferenceRule, not at an appended assertion.
    The legacy R7 presentation supplies the detailed prose for the very same
    isomorphism subgoal; it is not used to invent or replace any ProofStep.
    """
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

    source_group = _group_latex(iso.conclusion.map.source_group)
    target_group = _group_latex(iso.conclusion.map.target_group)
    target = _structure_latex(root.conclusion)
    source_eq = _structure_latex(source.conclusion)
    source_gen = _element_latex(source.conclusion.rhs.generator)
    target_gen = _element_latex(image.conclusion.rhs)
    references = _reference_section(existing_public_markdown)
    if references:
        # The source structure is an independently derived input, not a
        # premise proved in this group-structure proof's EHP subargument.
        references += (
            "\n\n**[R4] 既証明の群構造.**\n\n"
            + "$" + source_eq + "$."
        )
    heading = "# Group proof narrative\n\n## 証明対象\n\n$$\n" + target + "\n$$\n"
    if references:
        heading += "\n" + references + "\n"

    detailed_ehp = _phase162_legacy_ehp_body(existing_public_markdown)
    if detailed_ehp is None:
        # Focused callers without an existing prose presentation can still
        # render a proof, but may not claim that a full legacy paragraph was
        # supplied. Their steps and source/result relations remain checked.
        detailed_ehp = (
            "EHP 完全列\n\n"
            r"$\pi_{6}^{3}\xrightarrow{H}\pi_{6}^{5}"
            r"\xrightarrow{\Delta}\pi_{4}^{2}"
            r"\xrightarrow{E}\pi_{5}^{3}"
            r"\xrightarrow{H}\pi_{5}^{5}"
            r"\xrightarrow{\Delta}\pi_{3}^{2}$."
            "\n\n(5.3) の $H(\\nu')=\\eta_5$ と Proposition 5.1 の "
            "$\\pi_6^5=\\mathbb{Z}/2\\{\\eta_5\\}$ より, 左側の $H$ は全射である. "
            "完全性から $\\Delta:\\pi_6^5\\to\\pi_4^2$ は零写像となり, "
            "$E$ は単射である.\n\n"
            "また, Proposition 5.1 の $\\Delta(\\iota_5)=\\pm2\\eta_2$ と "
            "$\\pi_3^2=\\mathbb{Z}\\{\\eta_2\\}$, "
            "$\\pi_5^5=\\mathbb{Z}\\{\\iota_5\\}$ より, 右側の $\\Delta$ は単射である. "
            "完全性から右側の $H$ は零写像となり, $E$ は全射である."
        )
    conclusion = (
        "したがって, $\\ker E=\\operatorname{im}\\Delta=0$ かつ "
        "$\\operatorname{im}E=\\ker H=" + target_group + "$ である. "
        "ゆえに\n\n$$\nE:" + source_group + r"\xrightarrow{\cong}" + target_group
        + "\n$$\n\n"
    )
    if references:
        conclusion += "[R4] より, $" + source_eq + "$ が既知である.\n\n"
    else:
        conclusion += "既証明の群構造 $" + source_eq + "$ を用いる.\n\n"
    conclusion += (
        "また, $\\eta$-family の定義に基づく推論から "
        "$E(" + source_gen + ")=" + target_gen + "$ を得る. "
        "以上より, 同型 $E$ が位数2の生成元を $" + target_gen
        + "$ に移すので\n\n$$\n" + target + "\n$$\n\n□\n"
    )
    return Phase162R3Narrative(
        markdown=heading + "\n---\n\n## 証明\n\n" + detailed_ehp + "\n\n" + conclusion,
        root_step=root,
        ordered_steps=ancestors,
    )



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
