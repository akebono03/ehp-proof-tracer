# 変更コード全文

- 変更: `phase162_r3_narrative_connection.py`
- 新規ヘルパー: `_phase162_web_display_math_delimiters()` を `render_phase162_r3_narrative()` の直前に追加
- 変更関数: `render_phase162_r3_narrative()` の出力をWeb対応区切りへ変換
- import変更なし、クラス変更なし
- 新規テスト: `tests/test_phase162_r3_web_math_display.py`（ZIP内）

## 新規関数全文

```python
def _phase162_web_display_math_delimiters(markdown: str) -> str:
    r"""Convert delimiter-only $$ lines to the Web parser's \[ and \] blocks."""
    if not isinstance(markdown, str):
        raise TypeError("markdown must be a str")
    converted = []
    in_math = False
    for line in markdown.splitlines(keepends=True):
        if line.strip() != "$$":
            converted.append(line)
            continue
        newline = "\n" if line.endswith("\n") else ""
        converted.append((r"\]" if in_math else r"\[") + newline)
        in_math = not in_math
    if in_math:
        raise ValueError("Unterminated $$ math block in R3 narrative")
    return "".join(converted)
```

## 変更関数全文

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
        markdown=_phase162_web_display_math_delimiters(
            heading + "\n---\n\n## 証明\n\n" + detailed_ehp + "\n\n" + conclusion
        ),
        root_step=root,
        ordered_steps=ancestors,
    )
```

## テスト全文

```python
from phase162_r3_narrative_connection import (
    _phase162_web_display_math_delimiters,
)
from web_group_proof import _build_group_proof_rendered_lines


def test_r3_web_display_math_is_parsed_as_math():
    source = (
        "# Group proof narrative\n\n## 証明\n\n"
        "ゆえに\n\n$$\n"
        r"E:\pi_{4}^{2}\xrightarrow{\cong}\pi_{5}^{3}"
        "\n$$\n\n"
        "以上より\n\n$$\n"
        r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}"
        "\n$$\n\n□\n"
    )
    fixed = _phase162_web_display_math_delimiters(source)
    assert "$$" not in fixed
    assert fixed.count(r"\[") == 2
    assert fixed.count(r"\]") == 2
    lines = _build_group_proof_rendered_lines(fixed)
    math = [
        segment.value
        for line in lines
        for segment in line.segments
        if segment.kind == "display_math"
    ]
    assert len(math) == 2
    assert math[0] == r"E:\pi_{4}^{2}\xrightarrow{\cong}\pi_{5}^{3}"
    assert math[1] == r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}"


def test_r3_inline_math_and_reference_punctuation_unchanged():
    source = (
        "**[R1] Proposition 5.1.**\n"
        r"$\Delta(\iota_5)=\pm2\eta_2$."
        "\n\n$$\n"
        r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}"
        "\n$$\n"
    )
    fixed = _phase162_web_display_math_delimiters(source)
    assert "**[R1] Proposition 5.1.**" in fixed
    assert r"$\Delta(\iota_5)=\pm2\eta_2$." in fixed
    assert r"\pi_{5}^{3}=\mathbb{Z}/2\{\eta_{3}^{2}\}" in fixed


def test_r3_web_display_math_rejects_unclosed_block():
    import pytest
    with pytest.raises(ValueError, match="Unterminated"):
        _phase162_web_display_math_delimiters("## 証明\n\n$$\nE\n")
```
