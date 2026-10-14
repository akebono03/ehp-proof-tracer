# Phase 165-R56 変更後コード

## phase165_r52_partial_proof.py: render_partial_proof_markdown() 全文

```python
def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Use the existing whole-proof renderer for complete typed searches.

    Partial and failed searches retain their original fail-closed presentation.
    """
    from toda_group_proof_generic_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    if result.status is ProofSearchStatus.COMPLETE:
        from phase165_r56_presentation_adapter import render_completed_shared_narrative
        return render_completed_shared_narrative(result)
    return render_toda_partial_proof_narrative_markdown(result)
```

## phase165_r52_r3_web_adapter.py: import 全文

```python
"""Phase 165 R52-R3: common WebGroupProofView for partial proof states.

The adapter does not search for evidence, infer mathematical statements or
promote unproved goals into proven steps. Existing narrative rendering is
preserved for legacy complete proofs.
"""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus, render_partial_proof_markdown
from web_group_proof_common import (
    WebGroupProofStepView,
    WebGroupProofView,
    _build_group_proof_rendered_lines,
    _group_proof_rule_name,
    _group_proof_statement_latex,
)


```

## phase165_r52_r3_web_adapter.py: build_partial_web_group_proof_view() 全文

```python
def build_partial_web_group_proof_view(
    result: PartialProofResult,
    *,
    max_depth: int = 2,
    mode: str = "narrative",
) -> WebGroupProofView:
    """Adapt a verified search state to the shared Web view contract.

    Trace mode uses ProofStep entries only, while outline and narrative
    modes show the shared rendered text. Neither mode certifies open goals.
    """
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if isinstance(max_depth, bool) or not isinstance(max_depth, int):
        raise TypeError("max_depth must be an int")
    if max_depth < 0:
        raise ValueError("max_depth must be nonnegative")
    if mode not in ("trace", "outline", "narrative"):
        raise ValueError("mode must be trace, outline, or narrative")

    n = result.target.sphere_dimension
    dimension = result.target.group_dimension
    k = dimension - n
    target_latex = rf"\pi_{{{dimension}}}^{{{n}}}"

    steps = []
    for step in result.proven_steps:
        statement_latex, fallback_type_name = _group_proof_statement_latex(
            step.conclusion
        )
        steps.append(WebGroupProofStepView(
            depth=0,
            statement_latex=statement_latex,
            fallback_type_name=fallback_type_name,
            rule_name=_group_proof_rule_name(step),
            role_name="derived",
        ))

    if mode == "trace":
        rendered_lines = ()
    else:
        markdown = render_partial_proof_markdown(result)
        rendered_lines = _build_group_proof_rendered_lines(markdown)

    return WebGroupProofView(
        n=n,
        k=k,
        conclusion_latex=target_latex,
        theorem=None,
        phase="165 R52-R3",
        key="generic-partial-proof",
        steps=tuple(steps),
        max_depth=max_depth,
        mode=mode,
        rendered_lines=rendered_lines,
        partial_result=(result.status is not ProofSearchStatus.COMPLETE),
    )
```

## 新規関数とテスト

新規 `phase165_r56_presentation_adapter.py` の `render_completed_shared_narrative()` と、`test_phase165_r56_common_renderer.py` のテスト全文は同梱ファイルを参照。

## HTML 修正

旧 Group query の失敗表示は、完成した型付き証明がある場合に抑止。未完成の場合には保持。
