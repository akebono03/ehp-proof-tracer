# R57-R2 変更コード（省略なし）

変更先既存ファイルの import に変更なし。

## public renderer — 全文

```python
def render_toda_group_proof_narrative_markdown(
  presentation: TodaGroupProofPresentation,
) -> str:
  """The single public Narrative entry for complete and incomplete searches."""
  from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
  if isinstance(presentation, PartialProofResult):
    if presentation.status is ProofSearchStatus.COMPLETE:
      from phase165_r56_presentation_adapter import render_completed_shared_narrative
      return render_completed_shared_narrative(presentation)
    from phase165_r57_r2_partial_narrative import render_incomplete_public_narrative
    return render_incomplete_public_narrative(presentation)

  stable_transport_narrative = (
    _phase160_r7_render_stable_finite_cyclic_transport_narrative(
      presentation
    )
  )
  if stable_transport_narrative is not None:
    return stable_transport_narrative

  rendered = (
    _phase160_r7_previous_public_narrative_renderer(
      presentation
    )
  )
  from phase164_r9_narrative_contract import normalize_public_narrative_contract
  rendered = normalize_public_narrative_contract(
    suppress_toda_group_proof_narrative_dangling_connectors(
      rendered
    )
  )
  return rendered
```

## partial compatibility — 全文

```python
def render_partial_proof_markdown(result: PartialProofResult) -> str:
    """Compatibility API: use the one public Toda narrative renderer."""
    from toda_group_proof_narrative_renderer import (
        render_toda_group_proof_narrative_markdown,
    )
    return render_toda_group_proof_narrative_markdown(result)
```

## 新規関数・import・テスト全文

新規ファイル `phase165_r57_r2_partial_narrative.py`（ファイル先頭へ追加）の全文：

```python
"""Incomplete search states for the existing public Toda Narrative entry point.

A partial proof is not a TodaGroupProofPresentation: its unproved goals must
never be promoted to derivations, nor may a completed root be synthesized.
"""
from homotopy_groups import TodaPrimaryGroup
from phase165_r52_partial_proof import (
    GroupStructureStatus,
    PartialProofResult,
    ProofSearchStatus,
)
from toda_group_proof_generic_narrative_renderer import _render_generic_narrative_step
from web_group_proof_common import _group_proof_statement_latex


def _partial_statement_math(statement):
    if isinstance(statement, str):
        return statement
    latex, _fallback = _group_proof_statement_latex(statement)
    if latex is not None:
        return "$" + latex + "$"
    if isinstance(statement, TodaPrimaryGroup):
        return (
            f"$\\pi_{{{statement.group_dimension}}}"
            f"^{{{statement.sphere_dimension}}}$"
        )
    group = getattr(statement, "group", None)
    if isinstance(group, TodaPrimaryGroup):
        return _partial_statement_math(group) + " の群構造の決定"
    return type(statement).__name__ + "（数式表示未対応）"


def render_incomplete_public_narrative(result: PartialProofResult) -> str:
    """Render only verified steps and explicitly label unresolved obligations."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is ProofSearchStatus.COMPLETE:
        raise ValueError("completed search requires TodaGroupProofPresentation")

    status = {
        ProofSearchStatus.PARTIAL: "部分証明・未完成",
        ProofSearchStatus.SEARCH_FAILED: "証明未完成",
        ProofSearchStatus.NOT_SEARCHED: "未探索",
    }[result.status]
    target = _partial_statement_math(result.target)
    if result.open_goals:
        target = _partial_statement_math(result.open_goals[0])
    lines = ["## 証明対象", target, "", f"**探索状態：{status}**"]
    if result.structure_status is GroupStructureStatus.UNKNOWN:
        lines.append("群構造の証明状態: unknown（この探索では未確定）")
    if result.references:
        lines.extend(("", "## 使用する結果（Reference）"))
        for reference in result.references:
            lines.append("- " + reference)

    lines.extend(("", "## 証明（Proof（導出済み））"))
    used = set()
    for step in result.proven_steps:
        if id(step) in used:
            continue
        used.add(id(step))
        if isinstance(step.conclusion, str):
            lines.append(step.conclusion)
        else:
            lines.append(_render_generic_narrative_step(step))
    if not result.proven_steps:
        lines.append("証明できた数学的な ProofStep はまだありません。")

    if result.open_goals:
        lines.extend(("", "## 未解決 Goal"))
        for goal in result.open_goals:
            lines.append("- " + _partial_statement_math(goal))

    if result.diagnostics:
        lines.extend(("", "## 探索診断"))
        for diagnostic in result.diagnostics:
            if diagnostic.startswith("expected one registered derivation for "):
                lines.append("- この目標を導出する型付き Reference と推論規則の組み合わせが見つかりません。")
            elif "SOURCE_ARCHIVE" in diagnostic:
                lines.append("- 数学的に型付けされていない出典テキストは証明に利用していません。")
            else:
                lines.append("- " + diagnostic)

    if result.status is ProofSearchStatus.NOT_SEARCHED:
        lines.extend(("", "証明探索はまだ実行されていません。"))
    else:
        lines.extend(("", "未解決 Goal は証明済みの結論ではありません。"))
    return "\n".join(lines)
```

新規テスト `test_phase165_r57_r2_public_single_renderer.py` の import および関数全文：

```python
"""Targeted tests for the only public narrative entry point."""
import pytest

from phase165_r52_partial_proof import (
    ProofSearchStatus,
    make_partial_proof_result,
    render_partial_proof_markdown,
)
from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown


def test_r57_r2_partial_uses_public_renderer(monkeypatch):
    import toda_group_proof_narrative_renderer as public
    observed = []
    actual = public.render_toda_group_proof_narrative_markdown

    def delegate(argument):
        observed.append(argument)
        return actual(argument)

    monkeypatch.setattr(public, "render_toda_group_proof_narrative_markdown", delegate)
    result = make_partial_proof_result(
        n=3,
        k=1,
        status=ProofSearchStatus.PARTIAL,
        open_goals=("unresolved premise",),
    )
    rendered = render_partial_proof_markdown(result)
    assert observed == [result]
    assert "未解決 Goal" in rendered
    assert "unresolved premise" in rendered
    assert "□" not in rendered


def test_r57_r2_incomplete_public_entry_is_fail_closed():
    result = make_partial_proof_result(
        n=4,
        k=7,
        status=ProofSearchStatus.SEARCH_FAILED,
        open_goals=("unknown typed theorem",),
        diagnostics=("no matching typed inference",),
    )
    rendered = render_toda_group_proof_narrative_markdown(result)
    assert "証明未完成" in rendered
    assert "未解決 Goal" in rendered
    assert "no matching typed inference" in rendered
    assert "□" not in rendered


def test_r57_r2_complete_search_uses_existing_presentation(monkeypatch):
    import phase165_r56_presentation_adapter as adapter
    import toda_group_proof_narrative_renderer as public
    from phase165_r55_nk_only_goal import search_group_from_registered_goal
    result = search_group_from_registered_goal(n=2, k=1)
    assert result.status is ProofSearchStatus.COMPLETE
    seen = []
    real = adapter.render_completed_shared_narrative

    def observed(argument):
        seen.append(argument)
        return real(argument)

    monkeypatch.setattr(adapter, "render_completed_shared_narrative", observed)
    rendered = public.render_toda_group_proof_narrative_markdown(result)
    assert seen == [result]
    assert "使用する結果" in rendered
    assert "証明" in rendered
    assert "GeneratorSuspension" not in rendered


def test_r57_r2_public_entry_rejects_invalid_partial_type():
    from phase165_r57_r2_partial_narrative import render_incomplete_public_narrative
    with pytest.raises(TypeError):
        render_incomplete_public_narrative(None)
```
