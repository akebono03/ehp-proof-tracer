# R3-15 追加対象

- `phase168_r3_15_renderability_audit.py`: ZIP 内の監査モジュール。リポジトリ既存ファイルは変更しない。
- `tests/test_phase168_r3_15_renderability_audit.py`: 監査テスト。

## import・クラス・関数全文

```python
"""Audit actual typed ProofStep rendering coverage, without changing display."""
from __future__ import annotations
from dataclasses import dataclass
from phase165_r52_partial_proof import PartialProofResult
from phase168_r3_3_proof_narrative_model import ProofNarrativeModel
from phase168_r3_14_reasoned_narrative import build_reasoned_narrative_lines
from web_group_proof_common import _group_proof_statement_latex
from toda_proof_narrative_renderer import render_toda_proof_statement_latex
from toda_conclusion_latex_renderer import render_repository_conclusion_latex


@dataclass(frozen=True)
class RenderabilityFinding:
    step_index: int
    statement_type: str
    rule: str
    inference_name: str | None
    current_renderable: bool
    candidates: tuple[tuple[str, str | None, str | None], ...]


def _attempt(renderer, statement):
    try:
        value = renderer(statement)
    except Exception as error:
        return None, type(error).__name__
    if isinstance(value, str) and value.strip():
        return value, None
    return None, "empty_or_non_string"


def audit_reasoned_renderability(result: PartialProofResult, model: ProofNarrativeModel) -> tuple[RenderabilityFinding, ...]:
    """Compare existing renderers for every currently unsupported conclusion.

    A candidate being printable does not certify its semantic suitability.
    """
    lines = build_reasoned_narrative_lines(result, model)
    findings = []
    for line in lines:
        if line.conclusion_latex is not None:
            continue
        step = model.steps[line.step_index]
        # Evaluate candidate renderers independently. Do not accept a mere
        # fallback type string as mathematical LaTeX.
        a, error_a = _attempt(render_toda_proof_statement_latex, step.conclusion)
        c, error_c = _attempt(render_repository_conclusion_latex, step.conclusion)
        def web_render(statement):
            latex, fallback = _group_proof_statement_latex(statement)
            return latex if fallback is None else None
        w, error_w = _attempt(web_render, step.conclusion)
        findings.append(RenderabilityFinding(
            step_index=line.step_index,
            statement_type=type(step.conclusion).__name__,
            rule=step.rule.value if isinstance(step.rule.value, str) else step.rule.name,
            inference_name=getattr(step.inference_rule, 'name', None),
            current_renderable=False,
            candidates=(("toda_proof", a, error_a), ("repository", c, error_c), ("web", w, error_w)),
        ))
    return tuple(findings)

```

## テスト全文

```python
from unittest.mock import patch
from phase165_r52_partial_proof import ProofSearchStatus, make_partial_proof_result
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_15_renderability_audit import audit_reasoned_renderability, _attempt
from proof import ProofRule, ProofStep


def _case():
    step = ProofStep(conclusion=object(), premises=(), rule=ProofRule.GIVEN)
    result = make_partial_proof_result(n=2, k=1, status=ProofSearchStatus.PARTIAL, proven_steps=(step,))
    return result, build_proof_narrative_model(result)


def test_attempt_returns_latex():
    assert _attempt(lambda _: r"\pi_3^2", object()) == (r"\pi_3^2", None)


def test_attempt_handles_exception():
    value, error = _attempt(lambda _: 1 / 0, object())
    assert value is None and error == "ZeroDivisionError"


def test_attempt_rejects_nonstring():
    assert _attempt(lambda _: ("a",), object()) == (None, "empty_or_non_string")


def test_audit_tracks_each_renderer_independently():
    result, model = _case()
    with patch('phase168_r3_15_renderability_audit.build_reasoned_narrative_lines') as body, \
         patch('phase168_r3_15_renderability_audit.render_toda_proof_statement_latex', return_value='T'), \
         patch('phase168_r3_15_renderability_audit.render_repository_conclusion_latex', side_effect=TypeError('x')), \
         patch('phase168_r3_15_renderability_audit._group_proof_statement_latex', return_value=(None, 'Object')):
        body.return_value = (type('Line', (), {'step_index': 0, 'conclusion_latex': None})(),)
        found = audit_reasoned_renderability(result, model)
    assert len(found) == 1
    assert found[0].candidates[0][1] == 'T'
    assert found[0].candidates[1][2] == 'TypeError'
    assert found[0].candidates[2][1] is None

```
