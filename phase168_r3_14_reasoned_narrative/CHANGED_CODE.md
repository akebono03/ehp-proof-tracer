# 変更対象

新規クラス `NarrativeReasonedLine` と新規関数 `build_reasoned_narrative_lines` / `render_reasoned_narrative_markdown` は新規ファイル `phase168_r3_14_reasoned_narrative.py` 内に追加します。既存ファイルの変更なし。

## 新規コード全文

```python
"""Dependency-aware narrative projection from already proven ProofSteps.

No new theorem, source, or mathematical identity is inferred here.
"""
from __future__ import annotations

from dataclasses import dataclass

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_13_dependency_model import build_narrative_inferences
from proof import ProofRule
from web_group_proof_common import _group_proof_statement_latex


@dataclass(frozen=True)
class NarrativeReasonedLine:
    step_index: int
    premise_indices: tuple[int, ...]
    conclusion_latex: str | None
    premise_latex: tuple[str, ...]
    citation_numbers: tuple[int, ...]
    role: str


def build_reasoned_narrative_lines(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> tuple[NarrativeReasonedLine, ...]:
    """Project explicit dependencies into sentences without guessing reasons."""
    inferences = build_narrative_inferences(result, model)
    lines = []
    for item in inferences:
        if item.unresolved_premises:
            raise ValueError("unresolved premise: narrative cannot assert a derivation")
        step = model.steps[item.step_index]
        latex, fallback = _group_proof_statement_latex(step.conclusion)
        if fallback is not None:
            latex = None
        premise_latex = []
        for ancestor in item.premise_indices:
            premise, ancestor_fallback = _group_proof_statement_latex(
                model.steps[ancestor].conclusion
            )
            if premise is not None and ancestor_fallback is None:
                premise_latex.append(premise)
        role = ("given" if step.rule is ProofRule.GIVEN else
                "root" if item.is_root else "inference")
        lines.append(NarrativeReasonedLine(
            step_index=item.step_index,
            premise_indices=item.premise_indices,
            conclusion_latex=latex,
            premise_latex=tuple(premise_latex),
            citation_numbers=item.citation_numbers,
            role=role,
        ))
    return tuple(lines)


def render_reasoned_narrative_markdown(
    result: PartialProofResult,
    model: ProofNarrativeModel,
) -> str:
    """Render a verbose opt-in evidence trace with explicit premise links.

    This is not yet the final mathematical prose generator: unrenderable
    statements are identified by step number, never turned into guessed math.
    """
    lines = build_reasoned_narrative_lines(result, model)
    output = ["使用する結果", ""]
    for citation in model.citations:
        locator = citation.reference.locator or citation.reference.label
        output.extend((f"**[R{citation.number}] {locator}.**", ""))
    output.extend(("証明", ""))
    for line in lines:
        index = line.step_index + 1
        tags = ", ".join(f"[R{number}]" for number in line.citation_numbers)
        if line.role == "given":
            opening = f"{tags}より" if tags else "既知の命題として"
        elif line.premise_indices:
            refs = ", ".join(f"ステップ{item + 1}" for item in line.premise_indices)
            opening = f"{refs}を前提として"
            if tags:
                opening += f"、{tags}を用いて"
        else:
            opening = f"{tags}を用いて" if tags else "証明済みの推論により"
        if line.conclusion_latex is None:
            sentence = f"ステップ{index}：{opening}、型付き命題を導く（数式表示未対応）。"
        else:
            sentence = f"ステップ{index}：{opening}、${line.conclusion_latex}$ を得る。"
        output.extend((sentence, ""))
    if result.status is ProofSearchStatus.COMPLETE:
        output.append("□")
    return "\n".join(output).rstrip() + "\n"
```

## テスト import と関数全文

```python
from dataclasses import replace

import pytest

from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_14_reasoned_narrative import (
    build_reasoned_narrative_lines,
    render_reasoned_narrative_markdown,
)
from proof import InferenceRule, LiteratureReference, ProofRule, ProofStep


def _case():
    given = ProofStep("A", (), ProofRule.GIVEN)
    rule = InferenceRule(
        name="sample", literature_reference=LiteratureReference(
            label="Toda (5.2)", locator="(5.2)",
        ),
    )
    root = ProofStep("B", ("A",), ProofRule.INFERENCE, inference_rule=rule)
    result = make_partial_proof_result(
        n=2, k=2, status=ProofSearchStatus.COMPLETE,
        proven_steps=(given, root), conclusion="B",
    )
    return result, build_proof_narrative_model(result)


def test_dependency_is_preserved():
    result, model = _case()
    lines = build_reasoned_narrative_lines(result, model)
    assert len(lines) == 2
    assert lines[1].premise_indices == (0,)
    assert lines[1].citation_numbers == (1,)
    assert lines[1].role == "root"


def test_render_does_not_invent_mathematical_text():
    result, model = _case()
    markdown = render_reasoned_narrative_markdown(result, model)
    assert "[R1] (5.2)" in markdown
    assert "ステップ1を前提として" in markdown
    assert "数式表示未対応" in markdown
    assert "完全性より" not in markdown


def test_missing_premise_fails_closed():
    result, model = _case()
    wrong_step = replace(result.proven_steps[1], premises=("UNKNOWN",))
    changed = replace(result, proven_steps=(result.proven_steps[0], wrong_step))
    with pytest.raises(ValueError, match="unresolved premise"):
        render_reasoned_narrative_markdown(changed, build_proof_narrative_model(changed))


def test_inconsistent_model_fails_closed():
    result, model = _case()
    changed = replace(result, proven_steps=tuple(reversed(result.proven_steps)))
    with pytest.raises(ValueError, match="must match"):
        build_reasoned_narrative_lines(changed, model)
```
