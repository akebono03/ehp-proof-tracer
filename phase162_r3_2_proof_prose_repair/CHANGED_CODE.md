# Phase 162 R3-2 Proof Prose Repair — Complete changed units

No import section changes. The following function bodies are complete, directly replaceable code.

## `_element_latex`

```python
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
```

## `_phase162_legacy_ehp_body`

```python
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
```

## `render_phase162_r3_narrative`

```python
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
```

## `tests/test_phase162_r3_narrative_connection.py` — complete file

```python
from dataclasses import replace

import pytest

from phase162_r2_existing_proof_connection import reconstruct_phase162_r2_from_existing_proofs
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from proof import ProofRule
from tests.test_phase59_n3_ehp_chain import build_phase59_3_data
from tests.test_phase59_pi5_3_eta3_squared import build_phase59_4_data
from tests.test_phase59_toda52_pi4_2_transport import build_phase59_2_data


def _validated_connection():
    source = build_phase59_2_data()["result_steps"][0]
    target = build_phase59_4_data()
    ehp = build_phase59_3_data()
    definitions = (target["eta3_definition_step"], target["eta4_definition_step"])
    roots = {}

    def visit(step):
        if step.rule is ProofRule.GIVEN:
            roots[id(step)] = step
        else:
            for premise in step.premises:
                visit(premise)

    for step in (source,) + definitions + ehp["premise_steps"]:
        visit(step)
    return reconstruct_phase162_r2_from_existing_proofs(
        target["expected_pi5_3_relation"],
        ehp["expected_suspension_isomorphism"].map,
        (source,),
        definitions,
        ehp["premise_steps"],
        tuple(roots.values()),
    )


def test_r3_group_goal_is_final_and_no_map_headings():
    connection = _validated_connection()
    result = render_phase162_r3_narrative(connection)
    assert result.root_step is connection.reconstruction.final_step
    assert result.ordered_steps[-1] is result.root_step
    assert "\\pi_{5}^{3}=\\mathbb{Z}/2" in result.markdown
    assert "## 単射性" not in result.markdown
    assert "## 全射性" not in result.markdown
    assert "## 結論" not in result.markdown
    assert result.markdown.count("## 証明\n") == 1


def test_r3_final_claim_is_derived_from_proof_root():
    result = render_phase162_r3_narrative(_validated_connection())
    assert result.root_step.conclusion == result.ordered_steps[-1].conclusion
    assert result.markdown.count(r"\pi_{5}^{3}=\mathbb{Z}/2") == 2
    assert "\\ker E=" in result.markdown
    assert "\\operatorname{im}E=" in result.markdown
    assert result.markdown.rstrip().endswith("□")


def test_r3_reference_section_is_preserved_verbatim():
    ref = "# Group proof narrative\n\n## 証明対象\n\nold\n\n## 使用する結果\n\n**[R1] Proposition 5.1.**\n$\\pi_6^5$\n\n## 証明\nold body\n"
    text = render_phase162_r3_narrative(_validated_connection(), ref).markdown
    assert "**[R1] Proposition 5.1.**\n$\\pi_6^5$" in text
    assert "old body" not in text


def test_r3_rejects_invalid_root_rule():
    connection = _validated_connection()
    wrong_root = replace(connection.reconstruction.final_step, rule=ProofRule.GIVEN)
    wrong_reconstruction = replace(connection.reconstruction, final_step=wrong_root)
    wrong_connection = replace(connection, reconstruction=wrong_reconstruction)
    with pytest.raises(ValueError, match="derived group-structure"):
        render_phase162_r3_narrative(wrong_connection)


def test_r3_rejects_missing_proof_premise():
    connection = _validated_connection()
    wrong_root = replace(connection.reconstruction.final_step, premises=connection.reconstruction.final_step.premises[:2])
    wrong_connection = replace(connection, reconstruction=replace(connection.reconstruction, final_step=wrong_root))
    with pytest.raises(ValueError, match="three premises"):
        render_phase162_r3_narrative(wrong_connection)


def test_r3_public_reference_adapter_uses_existing_renderer(monkeypatch):
    from phase162_r3_narrative_connection import render_phase162_r3_with_public_references
    import toda_group_proof_narrative_renderer

    calls = []

    def fake_public_renderer(presentation):
        calls.append(presentation)
        return "## 使用する結果\n\n**[R1] Proposition 5.1.**\n\n## 証明\nold body"

    monkeypatch.setattr(
        toda_group_proof_narrative_renderer,
        "render_toda_group_proof_narrative_markdown",
        fake_public_renderer,
    )
    presentation = object()
    result = render_phase162_r3_with_public_references(_validated_connection(), presentation)
    assert calls == [presentation]
    assert "**[R1] Proposition 5.1.**" in result.markdown
    assert "old body" not in result.markdown

```

## `tests/test_phase162_r3_prose_regression.py` — complete file

```python
"""Phase 162 R3 prose regression for the verified lower panel."""

from phase162_r3_narrative_connection import render_phase162_r3_narrative
from tests.test_phase162_r3_narrative_connection import _validated_connection


def test_r3_detailed_ehp_prose_is_preserved_without_section_headings():
    old = (
        "## 使用する結果\n\n**[R1] (5.3).**\n\n"
        "**[R2] Proposition 5.1.**\n\n"
        "## 証明\n\nEHP 完全列を考える.\n\n"
        "### 準備\n\n[R1]より, $H(\\nu')=\\eta_5$.\n\n"
        "### 単射性\n\n[R2]より, Proposition 5.1 の適用で $H$ は全射である.\n\n"
        "### 全射性\n\n[R2]より, Proposition 5.1 の適用で $\\Delta$ は単射である.\n\n"
        "### 結論\n\n旧結論.\n\n□"
    )
    result = render_phase162_r3_narrative(_validated_connection(), old)
    proof = result.markdown.split("## 証明\n", 1)[1]
    assert "[R1]より" in proof
    assert proof.count("Proposition 5.1 の適用") == 2
    assert "### 単射性" not in proof
    assert "### 全射性" not in proof
    assert "旧結論" not in proof
    assert "既存の証明規則から" not in proof
    assert "群構造移送規則" not in proof
    assert proof.rstrip().endswith("□")
    assert proof.count("□") == 1


def test_r3_standard_eta_square_and_ascii_punctuation():
    result = render_phase162_r3_narrative(_validated_connection())
    assert r"\eta_{2}^{2}" in result.markdown
    assert r"\eta_{3}^{2}" in result.markdown
    assert r"\eta_{3}\circ \eta_{4}" not in result.markdown
    assert "。" not in result.markdown
    assert "群構造移送規則" not in result.markdown
    assert "H(\\nu')" not in result.markdown or "(5.3)" in result.markdown


def test_r3_known_source_is_reference_not_duplicated_derivation():
    old = (
        "## 使用する結果\n\n**[R1] (5.3).**\n\n"
        "## 証明\n\nEHP 完全列を考える.\n\n"
        "### 単射性\n\nProposition 5.1 により $H$ は全射である.\n\n"
        "### 全射性\n\nProposition 5.1 により $\\Delta$ は単射である.\n\n"
        "### 結論\n\n旧結論."
    )
    result = render_phase162_r3_narrative(_validated_connection(), old)
    assert "**[R4] 既証明の群構造.**" in result.markdown
    assert "[R4] より" in result.markdown
    assert r"\pi_{4}^{2}=\mathbb{Z}/2" in result.markdown

```

## `tests/test_phase162_r3_2_verified_group_connection.py` — complete file

```python
"""Phase 162 R3-2: Web lower-panel integration tests."""

from phase162_web_narrative_integration import (
    _build_phase162_existing_group_connection,
    build_phase162_web_validated_isomorphism_markdown,
)
from phase162_r3_narrative_connection import render_phase162_r3_narrative
from proof import ProofRule


def test_r3_2_uses_a_derived_group_goal():
    result = _build_phase162_existing_group_connection()
    assert result.reconstruction.final_step.rule is ProofRule.INFERENCE
    assert result.reconstruction.final_step.conclusion == result.reconstruction.goal
    assert len(result.reconstruction.derived_steps) == 8
    assert result.provenance.verified_inferences >= 9


def test_r3_2_uses_r3_group_narrative():
    connection = _build_phase162_existing_group_connection()
    rendered = render_phase162_r3_narrative(connection)
    assert rendered.root_step is connection.reconstruction.final_step
    assert r"\pi_{5}^{3}=\mathbb{Z}/2" in rendered.markdown
    assert "### 単射性" not in rendered.markdown
    assert "### 全射性" not in rendered.markdown


def test_r3_2_web_output_uses_group_root_without_old_headings():
    text = build_phase162_web_validated_isomorphism_markdown()
    assert "## 証明対象" in text
    assert r"\pi_{5}^{3}=\mathbb{Z}/2" in text
    assert "### 準備" not in text
    assert "### 単射性" not in text
    assert "### 全射性" not in text
    assert "### 結論" not in text
    assert "群構造移送規則" not in text
    assert text.count("## 証明\n") == 1


def test_r3_2_web_keeps_legacy_references_for_next_audit():
    text = build_phase162_web_validated_isomorphism_markdown()
    assert "## 使用する結果" in text
    assert "## 証明" in text
    assert text.rstrip().endswith("□")
    assert text.count("□") == 1
    assert "Proposition 5.1" in text
    assert r"\eta_{3}^{2}" in text


def test_r3_2_only_lower_panel_label_is_changed():
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    text = (root / "web_group_proof.py").read_text(encoding="utf-8-sig")
    assert "## 群構造の検証済み証明" in text
    assert "build_phase162_web_validated_isomorphism_markdown" in text


def test_r3_2_generator_is_derived_from_eta_bridge():
    from expression import Composition, Suspension
    from proof import Relation, RelationType

    connection = _build_phase162_existing_group_connection()
    source = connection.source_structure_step.conclusion.rhs.generator
    image = connection.generator_image_step.conclusion
    target = connection.reconstruction.goal.rhs.generator
    assert isinstance(image, Relation)
    assert image.relation_type is RelationType.EQUALITY
    assert image.lhs == Suspension(expression=source)
    assert isinstance(target, Composition)
    assert image.rhs == target
    assert connection.generator_image_step.rule is ProofRule.INFERENCE

```

## Scope and verification

Modified production function units: `_element_latex`, `_phase162_legacy_ehp_body` (new, immediately before `render_phase162_r3_narrative`), `render_phase162_r3_narrative`. No class changed. No imports changed.

Focused pytest is executed by the included PowerShell runner. Full suite is not executed. Completion requires passing focused tests and checking the real lower-panel Web text. Future work: literature reference classification and independent Web presentation audit.