# 変更対象とコード全文

変更対象：`tests/test_phase162_r2_validated_proof_presentation.py` の2つのテスト関数内部 import のみ（関数本体・検査内容はそのまま）。

変更後の両 import ブロック全文：

```python
from toda_group_proof_narrative_renderer import (
    _render_generic_narrative_step,
)
```

新規 `install.py`、`test_install.py`、`run.ps1`、`restore.ps1` の全文は同梱の実ファイルを参照。テスト関数は新規 `test_install.py` に全体を収録。既存テストの関数本体は変更せず、同一の import 文2箇所のみを AST で検査して置換する。

## 変更する既存テスト関数の全体（GitHub 監査時点、import のみ変更）

```python
def test_phase162_r2_text_is_rendered_by_common_step_renderer():
    from toda_group_proof_narrative_renderer import (
        _render_generic_narrative_step,
    )
    from toda_group_proof_narrative_renderer import (
        _render_group_proof_narrative_latex,
    )

    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    text = render_validated_backward_proof_markdown(presentation)
    reference, body = text.split("## 証明", 1)
    fixed_ids = {
        id(step)
        for entry in build_validated_proof_reference_entries(presentation)
        for step in entry.proof_steps
    }
    body_lines = body.splitlines()

    for step in presentation.nodes:
        if step.rule is not ProofRule.INFERENCE:
            continue
        generic = _render_generic_narrative_step(step)
        fallback = (
            step.inference_rule.name if step.inference_rule is not None else None
        )
        from expression import IteratedSuspension
        from proof import Relation, RelationType
        from repository_element_presentation import render_repository_conclusion_latex
        conclusion = step.conclusion
        if (
            isinstance(conclusion, Relation)
            and conclusion.relation_type is RelationType.EQUALITY
            and (
                isinstance(conclusion.lhs, IteratedSuspension)
                or isinstance(conclusion.rhs, IteratedSuspension)
            )
        ):
            expected = "$" + render_repository_conclusion_latex(conclusion) + "$"
        elif generic and generic != fallback and generic != f"`{type(step.conclusion).__name__}`":
            expected = generic
        else:
            latex = _render_group_proof_narrative_latex(step)
            assert latex is not None
            expected = "$" + latex + "$"
        assert _render_validated_backward_step(step) == expected
        if id(step) in fixed_ids:
            from toda_general_reference_schema import (
                get_general_reference_statement,
                render_general_reference_statement_lines,
            )
            from toda_literature_statement_boundary import classify_toda_literature_statement_step
            boundary = classify_toda_literature_statement_step(step)
            general = get_general_reference_statement(boundary.reference_locator)
            if general is None:
                assert expected.rstrip(".") in reference
            else:
                assert all(line in reference for line in render_general_reference_statement_lines(boundary.reference_locator))
        else:
            assert isinstance(expected, str) and expected
    sections = _composed_validated_proof_sections(
        presentation, frozenset(fixed_ids)
    )
    expected_body_lines = [
        line
        for heading, prose_lines in sections
        for line in (
            (("### " + heading,) if heading != "証明" else ()) + prose_lines
        )
    ]
    assert [line for line in body_lines if line and line != "□"] == expected_body_lines
    assert_composed_steps_preserved(
        [line for _, prose_lines in sections for line in prose_lines],
        _validated_proof_body_lines(presentation, frozenset(fixed_ids)),
    )
    assert text.rstrip().endswith("□")


def test_phase162_r2_whitehead_square_uses_existing_latex_renderer():
    from toda_group_proof_narrative_renderer import (
        _render_generic_narrative_step,
    )
    from toda_group_proof_narrative_renderer import (
        _render_group_proof_narrative_latex,
    )
    from toda_rules import TodaPi32WhiteheadSquareUpToSignStatement

    presentation = build_validated_backward_proof_presentation(_validated_fixture())
    whitehead = next(
        step for step in presentation.nodes
        if isinstance(step.conclusion, TodaPi32WhiteheadSquareUpToSignStatement)
    )
    assert _render_generic_narrative_step(whitehead) == whitehead.inference_rule.name
    latex = _render_group_proof_narrative_latex(whitehead)
    assert latex is not None
    assert r"\pm" in latex
    assert _render_validated_backward_step(whitehead) == "$" + latex + "$"
```
