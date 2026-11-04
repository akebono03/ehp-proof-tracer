# R15R16R2: 変更単位の全文

## 変更対象

- 既存 `phase173_r4_r15r9_shared_abstract_renderer/projection.py`: `_verified_abstract_progress_lines` 全体置換。
- 新規 `phase173_r4_r15r16r2_shared_tree_narrative/tree_adapter.py`: import と新規関数 `verified_tree_postorder`, `render_verified_tree_progress` 全文。既存の共有 Renderer は変更なし。
- 旧 `phase173_r4_r15r16_verified_progress_punctuation/tests/test_integration.py`: `test_abstract_certificate_displays_actual_verified_milestones` を全文置換。他のテスト変更なし。
- `run.ps1`, `install.py`, `patches.py`: 新規。

## 既存関数の置換後全文

```python
def _verified_abstract_progress_lines(
    structure: CertifiedAbstractStructure,
) -> tuple[str, ...]:
    """Render the existing certificate via the same common Narrative renderer.

    No proof-specific prose, four-premise assumption, or new inference.
    """
    from phase173_r4_r15r16r2_shared_tree_narrative.tree_adapter import (
        render_verified_tree_progress,
    )

    return render_verified_tree_progress(
        structure.group, structure.proof_step,
    )
```

## 新規アダプターの import・関数全文

```python
"""Render any already-verified proof subtree with the canonical Narrative Model.

This adapter owns no statement-specific sentences and no source discovery.
The original searched result remains intact; the scoped display view exists
only to feed a second verified tree to the *same* public model renderer.
"""
from __future__ import annotations

from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
from phase168_r3_3_proof_narrative_model import build_proof_narrative_model
from phase168_r3_5_model_renderer import render_model_backed_narrative_markdown
from proof import ProofRule, ProofStep


def verified_tree_postorder(root: ProofStep) -> tuple[ProofStep, ...]:
    """Visit every actual premise once, with cycle and inference guards."""
    if not isinstance(root, ProofStep):
        raise TypeError("root must be a ProofStep")
    active: set[int] = set()
    visited: set[int] = set()
    ordered: list[ProofStep] = []

    def visit(step: ProofStep) -> None:
        if not isinstance(step, ProofStep):
            raise TypeError("proof ancestry contains a non-ProofStep")
        identity = id(step)
        if identity in active:
            raise ValueError("cyclic proof ancestry")
        if identity in visited:
            return
        active.add(identity)
        if step.rule is ProofRule.GIVEN and step.premises:
            raise ValueError("a given step cannot consume premises")
        if step.rule is ProofRule.INFERENCE:
            rule = step.inference_rule
            if rule is None:
                raise ValueError("an inferred step requires its actual inference rule")
            guard = rule.match_guard
            if guard is not None and not guard(step.premises, ()):
                raise ValueError("unverified inference guard in proof ancestry")
        for premise in step.premises:
            visit(premise)
        active.remove(identity)
        visited.add(identity)
        ordered.append(step)

    visit(root)
    if not ordered or ordered[-1] is not root:
        raise ValueError("verified root missing from the ordered ancestry")
    return tuple(ordered)


def render_verified_tree_progress(
    target: TodaPrimaryGroup,
    root: ProofStep,
) -> tuple[str, ...]:
    """Reuse the exact canonical model-backed renderer for a certified tree.

    This presentation-only scope is not a second search and cannot create a
    named-group conclusion. Its public output is limited to source-backed
    Reference entries and renderable ProofSteps. Unsupported GIVEN types stay
    in the proof tree but are not fabricated into mathematical assertions.
    """
    if not isinstance(target, TodaPrimaryGroup):
        raise TypeError("target must be a TodaPrimaryGroup")
    steps = verified_tree_postorder(root)
    if root.rule is not ProofRule.INFERENCE:
        raise ValueError("a verified evidence root must be an inference")
    # This view is never published as a search result or used to decide status.
    # The real PartialProofResult retains all named open goals and diagnostics.
    scope = PartialProofResult(
        target=target,
        status=ProofSearchStatus.PARTIAL,
        proven_steps=steps,
    )
    model = build_proof_narrative_model(scope)
    markdown = render_model_backed_narrative_markdown(scope, model)
    reference_header = "## 使用する結果"
    proof_header = "## 証明"
    step_header = "### 確認済み ProofStep（与件を含む）"
    heading_lines = markdown.splitlines()
    if (heading_lines.count(reference_header) != 1
            or heading_lines.count(proof_header) != 1
            or heading_lines.count(step_header) != 1):
        raise ValueError("canonical renderer output has changed")
    source_section = markdown.split(reference_header, 1)[1].split("\n---\n", 1)[0]
    body_section = markdown.split(step_header, 1)[1]
    source_lines = [line.strip() for line in source_section.splitlines() if line.strip()]
    if "参照情報を持つ ProofStep はありません。" in source_lines:
        source_lines.remove("参照情報を持つ ProofStep はありません。")
    if not model.citations:
        raise ValueError("verified tree has no source-backed Reference")
    if not any(f"[R{citation.number}]" in line for line in source_lines
               for citation in model.citations):
        raise ValueError("the shared renderer dropped proof-tree citations")
    proof_lines = [
        line.strip() for line in body_section.splitlines()
        if line.lstrip().startswith(("- 与件:", "- 推論:"))
        and "（数式表示未対応）" not in line
    ]
    if not proof_lines:
        raise ValueError("verified evidence tree has no renderable ProofStep")
    return tuple([
        "### 検証済み証明木の Reference", "",
        *source_lines, "",
        "### 検証済み ProofStep", "",
        *proof_lines,
    ])
```

## 変更するテスト関数全文

既存テストファイルの import は変更しない。

```python
@pytest.mark.parametrize("k", (8, 9, 15, 31))
def test_abstract_certificate_displays_actual_verified_milestones(k: int) -> None:
    goal = exact_prior_database_result(4, k)
    assert goal is not None
    result = search_group_from_registered_goal(n=4, k=k, goal=goal)
    assert result.status in (ProofSearchStatus.PARTIAL, ProofSearchStatus.SEARCH_FAILED)
    assert result.conclusion is None and result.open_goals
    assert result.abstract_structure is not None
    assert result.abstract_structure.proof_step not in result.proven_steps

    model = build_proof_narrative_model(result)
    progress = render_certified_abstract_model_section(model)
    assert progress == render_certified_abstract_section(result)
    assert "## 検証済みの途中経過" in progress
    assert "### 検証済み証明木の Reference" in progress
    assert "### 検証済み ProofStep" in progress
    assert "Proposition 4.4" in progress
    assert "Lemma 5.4" in progress
    assert progress.count("DB prior: sphere.csv") >= 2
    assert "## 証明済みの抽象群構造" in progress
    assert "記名生成元の対応は未証明" in progress
    assert "先行データベースの " not in progress
    assert "Proposition 4.4 の適用前提となる定理を検証した" not in progress
    assert progress in render_model_backed_narrative_markdown(result, model)

    view = build_standard_web_group_proof_view(
        n=4, k=k, goal=goal, mode="narrative", citation_source="model",
    )
    assert view.partial_result and view.abstract_structure_certified
    assert view.key == "generic-partial-proof"
    headings = [line.prefix for line in view.rendered_lines if line.kind == "heading"]
    assert headings.count("検証済みの途中経過") == 1
    assert headings.count("証明済みの抽象群構造") == 1
    assert headings.count("未解決 Goal") == 1
    shown = "\n".join(
        seg.value for line in view.rendered_lines for seg in line.segments
    )
    assert "sphere.csv" in shown and "Lemma 5.4" in shown
    assert "Relation(lhs=" not in shown
    assert "、" not in shown and "。" not in shown
    assert result.conclusion is None and result.open_goals
```
