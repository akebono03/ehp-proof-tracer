# R57-R21 変更コード全文

変更対象:
- `toda_group_proof_generic_narrative_renderer.py` の `render_toda_partial_proof_narrative_markdown` 全体（import の変更なし）。
- `phase165_r56_presentation_adapter.py` の import 部分と `render_completed_shared_narrative` 全体（ファイル全体を置換）。
- 新規 `test_phase165_r57_r21_narrative_unification.py`（6 テスト、import 全文）。
- 新規 `install.py`、`run.ps1`。

## 共通 Renderer の置換関数全体

```python
def render_toda_partial_proof_narrative_markdown(result) -> str:
  """One source-faithful narrative for complete and incomplete typed searches.

  Search state only controls the ending. Both statuses use the same target,
  cited GIVEN ancestry, inferred ProofSteps and ordering. No proof is inferred
  from formatting, and an open goal never becomes a proved statement.
  """
  from homotopy_groups import TodaPrimaryGroup
  from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus
  from proof import ProofRule
  from web_group_proof_common import _group_proof_statement_latex

  if not isinstance(result, PartialProofResult):
    raise TypeError("result must be PartialProofResult")

  def statement_math(statement):
    if isinstance(statement, str):
      return statement
    latex, _fallback = _group_proof_statement_latex(statement)
    if latex is not None:
      return "$" + latex + "$"
    if isinstance(statement, TodaPrimaryGroup):
      return (f"$\\pi_{{{statement.group_dimension}}}"
              f"^{{{statement.sphere_dimension}}}$")
    return type(statement).__name__ + "（数式表示未対応）"

  def label(step):
    inference = getattr(step, "inference_rule", None)
    ref = getattr(inference, "literature_reference", None)
    locator = getattr(ref, "locator", None) or getattr(ref, "label", None)
    if locator:
      return str(locator)
    name = getattr(inference, "name", "") or ""
    if name.startswith("Adopted literature "):
      return name[len("Adopted literature "):]
    return None

  def unique_steps(steps):
    seen = set()
    ordered = []
    for step in steps:
      if id(step) not in seen:
        seen.add(id(step))
        ordered.append(step)
    return tuple(ordered)

  steps = unique_steps(result.proven_steps)
  if result.status is ProofSearchStatus.COMPLETE:
    roots = tuple(step for step in steps if step.conclusion == result.conclusion)
    if len(roots) != 1 or roots[0].rule is not ProofRule.INFERENCE:
      raise ValueError("a completed narrative requires exactly one inference root")
    if getattr(result.conclusion, "lhs", None) != result.target:
      raise ValueError("completed proof conclusion does not match target")
    from phase165_r57_r10_step_narrative import ordered_proof_ancestry
    steps = ordered_proof_ancestry(roots[0])

  target_statement = result.conclusion if result.status is ProofSearchStatus.COMPLETE else None
  if target_statement is None:
    candidate_goals = tuple(
      goal for goal in result.open_goals
      if getattr(goal, "lhs", None) == result.target
    )
    if candidate_goals:
      target_statement = candidate_goals[-1]
  if target_statement is None:
    target_statement = result.target

  lines = ["## 証明対象", "", statement_math(target_statement), "",
           "## 使用する結果", ""]
  citation_numbers = {}
  for step in steps:
    if step.rule is not ProofRule.GIVEN:
      continue
    locator = label(step)
    if locator is None:
      continue
    if locator not in citation_numbers:
      citation_numbers[locator] = "[R" + str(len(citation_numbers) + 1) + "]"
      lines.append("**" + citation_numbers[locator] + " " + locator + ".**")
      lines.append("")
  if not citation_numbers:
    lines.append("参照情報を持つ ProofStep はありません。")
    lines.append("")

  lines.extend(["---", "", "## 証明", ""])
  if not steps:
    lines.append("証明できた数学的な ProofStep はまだありません。")
    lines.append("")
  for step in steps:
    if step.rule is ProofRule.GIVEN:
      locator = label(step)
      prefix = citation_numbers[locator] + "より, " if locator in citation_numbers else "前提（出典情報未接続）: "
    else:
      refs = tuple(dict.fromkeys(
        citation_numbers[loc] for premise in step.premises
        for loc in (label(premise),) if loc in citation_numbers
      ))
      prefix = ("、".join(refs) + "より, ") if refs else ""
    rendered = _render_generic_narrative_step(step)
    if rendered:
      lines.append(prefix + rendered)
      lines.append("")

  if result.status is ProofSearchStatus.COMPLETE:
    lines.append("以上より, " + statement_math(result.conclusion) + ". □")
  else:
    state = {
      ProofSearchStatus.PARTIAL: "部分証明・未完成",
      ProofSearchStatus.SEARCH_FAILED: "証明未完成",
      ProofSearchStatus.NOT_SEARCHED: "未探索",
    }[result.status]
    lines.extend(["**探索状態：" + state + "**", ""])
    if result.open_goals:
      lines.extend(["## 未解決 Goal", ""])
      for goal in result.open_goals:
        lines.append("- " + statement_math(goal))
      lines.append("")
    if result.diagnostics:
      lines.extend(["## 探索診断", ""])
      for diagnostic in result.diagnostics:
        if diagnostic.startswith("expected one registered derivation for "):
          lines.append("- 型付き Reference と推論規則から一意な導出が見つかりません。")
        else:
          lines.append("- " + diagnostic)
      lines.append("")
    lines.append("未解決 Goal は証明済みの結論ではありません。")
  return "\n".join(lines)
```

## 完成証明 Adapter の変更後全文（import 全文を含む）

```python
"""Completed canonical proof searches use the same narrative as partial searches."""
from __future__ import annotations

from phase165_r52_partial_proof import PartialProofResult, ProofSearchStatus


def render_completed_shared_narrative(result: PartialProofResult) -> str:
    """Preserve the public completed entry while sharing the proof text path."""
    if not isinstance(result, PartialProofResult):
        raise TypeError("result must be PartialProofResult")
    if result.status is not ProofSearchStatus.COMPLETE or result.conclusion is None:
        raise ValueError("a complete search is required")
    if getattr(result.conclusion, "lhs", None) != result.target:
        raise ValueError("completed target does not match conclusion")
    from toda_group_proof_generic_narrative_renderer import (
        render_toda_partial_proof_narrative_markdown,
    )
    return render_toda_partial_proof_narrative_markdown(result)
```

## 新規テスト全文

```python
"""R57-R21: completed and incomplete search share one evidence-based Narrative."""
from __future__ import annotations

from pathlib import Path

from phase165_r52_partial_proof import ProofSearchStatus, render_partial_proof_markdown
from phase165_r55_nk_only_goal import search_group_from_registered_goal
from phase165_r56_presentation_adapter import render_completed_shared_narrative


def _root():
    return Path(__file__).resolve().parent.parent


def test_r21_completed_and_partial_public_paths_share_one_renderer():
    completed = search_group_from_registered_goal(n=2, k=1)
    assert completed.status is ProofSearchStatus.COMPLETE
    assert render_completed_shared_narrative(completed) == render_partial_proof_markdown(completed)


def test_r21_completed_has_single_common_sections_and_only_proved_final():
    completed = search_group_from_registered_goal(n=2, k=1)
    markdown = render_partial_proof_markdown(completed)
    assert markdown.count("## 証明対象") == 1
    assert markdown.count("## 使用する結果") == 1
    assert markdown.count("## 証明\n") == 1
    assert markdown.count("以上より") == 1
    assert markdown.endswith("□")
    assert "未解決 Goal" not in markdown
    assert "(5.1)" in markdown


def test_r21_partial_target_remains_original_group_goal():
    partial = search_group_from_registered_goal(n=3, k=1)
    assert partial.status is not ProofSearchStatus.COMPLETE
    rendered = render_partial_proof_markdown(partial)
    heading = rendered.split("## 証明対象", 1)[1].split("## 使用する結果", 1)[0]
    assert "\\pi_{4}^{3}" in heading or "π43" in heading or "π_4^3" in heading
    assert "\\pi_{5}^{5}" not in heading
    assert "未解決 Goal" in rendered
    assert "□" not in rendered


def test_r21_partial_and_completed_share_section_order():
    for n in (2, 3):
        text = render_partial_proof_markdown(search_group_from_registered_goal(n=n, k=1))
        assert text.index("## 証明対象") < text.index("## 使用する結果") < text.index("## 証明\n")


def test_r21_completed_entry_has_no_legacy_replay_or_legacy_renderer():
    code = (_root() / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    assert "build_complete_toda_group_result_proof_replay" not in code
    assert "render_toda_group_proof_narrative_markdown" not in code
    assert "render_toda_partial_proof_narrative_markdown" in code


def test_r21_unchanged_mathematics_and_no_group_specific_renderer_branches():
    code = (_root() / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    assert "n == 2" not in code
    assert "n == 3" not in code
    assert "ProofStep(" not in code
    assert "ProofRule.GIVEN" not in code
```

## Installer 全文

```python
"""Install R57-R21 without modifying search mathematics or old renderer sources."""
from __future__ import annotations

import ast
from pathlib import Path
import shutil


def _function(source: str, name: str) -> tuple[ast.FunctionDef, str]:
    tree = ast.parse(source)
    found = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == name]
    if len(found) != 1:
        raise RuntimeError("expected one function: " + name)
    node = found[0]
    return node, "".join(source.splitlines(keepends=True)[node.lineno - 1:node.end_lineno])


def install(project: Path, package: Path) -> str:
    renderer_path = project / "toda_group_proof_generic_narrative_renderer.py"
    adapter_path = project / "phase165_r56_presentation_adapter.py"
    if not all(p.is_file() for p in (renderer_path, adapter_path)):
        raise FileNotFoundError("required existing Narrative modules are missing")
    renderer_before = renderer_path.read_text(encoding="utf8")
    adapter_before = adapter_path.read_text(encoding="utf8")
    renderer_new = (package / "render_toda_partial_proof_narrative_markdown.py.txt").read_text(encoding="utf8")
    adapter_new = (package / "phase165_r56_presentation_adapter.py").read_text(encoding="utf8")
    _, old_function = _function(renderer_before, "render_toda_partial_proof_narrative_markdown")
    _, new_function = _function(renderer_new, "render_toda_partial_proof_narrative_markdown")
    if old_function != new_function:
        if ("target = statement_math(result.open_goals[0])" not in old_function
                or "_render_generic_narrative_step" not in old_function):
            raise RuntimeError("unexpected partial renderer version; no modification")
    _, old_adapter = _function(adapter_before, "render_completed_shared_narrative")
    if adapter_before != adapter_new and (
        "build_complete_toda_group_result_proof_replay" not in old_adapter
        or "render_toda_group_proof_narrative_markdown" not in old_adapter
    ):
        raise RuntimeError("unexpected completed renderer version; no modification")
    node, _ = _function(renderer_before, "render_toda_partial_proof_narrative_markdown")
    lines = renderer_before.splitlines(keepends=True)
    updated_renderer = "".join(lines[:node.lineno - 1]) + new_function.rstrip() + "\n" + "".join(lines[node.end_lineno:])
    ast.parse(updated_renderer)
    ast.parse(adapter_new)
    if updated_renderer == renderer_before and adapter_new == adapter_before:
        return "ALREADY_INSTALLED"
    for target, content in ((renderer_path, updated_renderer), (adapter_path, adapter_new)):
        if target.read_text(encoding="utf8") != content:
            backup = target.with_name(target.name + ".phase165_r57_r21_backup")
            if not backup.exists():
                shutil.copy2(target, backup)
            target.write_text(content, encoding="utf8")
    return "INSTALLED"


if __name__ == "__main__":
    package = Path(__file__).resolve().parent
    print("R57-R21:", install(package.parent, package))
    print("One common completed/partial Narrative path; full pytest NOT run")
```

## PowerShell 全文

```powershell
$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Set-Location $project
$python = if (Get-Command python -ErrorAction SilentlyContinue) { 'python' } elseif (Get-Command py -ErrorAction SilentlyContinue) { 'py' } else { throw 'Python was not found' }
& $python (Join-Path $package 'install.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21 install failed' }
& $python -m pytest -q (Join-Path $package 'test_phase165_r57_r21_narrative_unification.py')
if ($LASTEXITCODE -ne 0) { throw 'R57-R21 targeted pytest failed' }
Write-Output 'R57-R21 targeted tests passed; full pytest NOT run.'
```

実行する pytest: `python -m pytest -q phase165_r57_r21_narrative_unification/test_phase165_r57_r21_narrative_unification.py`。
完了条件: 二つの入口で同じ本文、原目標の保持、完了時のみ □、未完成時の未解決表示。
次 Phase 境界: 完全列の型付き利用、未対応 statement の数式表示、および ProofStep 由来の自然文の高度化。
