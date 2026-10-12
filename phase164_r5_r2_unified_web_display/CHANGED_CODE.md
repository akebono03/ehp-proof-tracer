# Phase 164 R5-R2 — 変更コード全文

変更対象：
- `web_group_proof.py`: `build_standard_web_group_proof_view()` の全体置換。import 変更なし。
- `phase164_r5_r2_common_replay.py`: 新規モジュール。ファイル先頭に追加。
- `tests/test_phase164_r5_r2_unified_web_display.py`: 新規テスト。
- `apply_patch.py`, `sweep_112.py`, `run.ps1`: 新規。

証明の内容・共通 Renderer 本体・既存の API は変更しない。

## web_group_proof.py の置換関数

```python
def build_standard_web_group_proof_view(
  n: int,
  k: int,
  max_depth: int = 2,
  mode: str = "narrative",
) -> WebGroupProofView:
  """Render every group through the same presentation and narrative pipeline."""
  query = TodaGroupQuery(n=n, k=k)
  domain = classify_toda_group_query_domain(query)
  if domain.kind is not TodaGroupQueryDomainKind.POSITIVE_DIMENSION:
    raise ValueError("group proof is available only for repository-backed group results")
  if isinstance(max_depth, bool) or not isinstance(max_depth, int):
    raise TypeError("max_depth must be an int")
  if max_depth < 0:
    raise ValueError("max_depth must be nonnegative")
  if mode not in ("trace", "outline", "narrative"):
    raise ValueError("mode must be trace, outline, or narrative")

  report = build_standard_toda_report(n=n, k=k)
  if report.status is TodaCalculationStatus.NOT_FOUND:
    raise ValueError("no proof-backed group result found")
  if report.status is TodaCalculationStatus.MULTIPLE_RESULTS:
    raise ValueError("group proof requires exactly one result")
  group_result = report.candidates[0].source_candidate.group_result

  from phase164_r5_r2_common_replay import build_phase164_r5_r2_common_replay
  replay = build_phase164_r5_r2_common_replay(
    n=n, k=k, group_result=group_result, max_depth=max_depth, mode=mode,
  )

  conclusion_latex, conclusion_fallback = _group_proof_statement_latex(
    replay.root_step.conclusion
  )
  if conclusion_latex is None:
    raise ValueError(
      "group conclusion is not renderable as LaTeX: "
      f"{conclusion_fallback}"
    )

  steps = []
  for replay_step in replay.steps:
    statement_latex, fallback_type_name = _group_proof_statement_latex(
      replay_step.proof_step.conclusion
    )
    steps.append(WebGroupProofStepView(
      depth=replay_step.depth,
      statement_latex=statement_latex,
      fallback_type_name=fallback_type_name,
      rule_name=_group_proof_rule_name(replay_step.proof_step),
      role_name=replay_step.role.value,
    ))

  rendered_lines = ()
  if mode != "trace":
    presentation = build_toda_group_proof_presentation(replay)
    if mode == "outline":
      markdown = render_toda_group_proof_outline_markdown(presentation)
    else:
      markdown = render_toda_group_proof_narrative_markdown(presentation)
    rendered_lines = _build_group_proof_rendered_lines(markdown)

  return WebGroupProofView(
    n=n,
    k=k,
    conclusion_latex=conclusion_latex,
    theorem=replay.source_entry.theorem,
    phase=replay.source_entry.phase,
    key=replay.source_entry.key,
    steps=tuple(steps),
    max_depth=replay.max_depth,
    mode=mode,
    rendered_lines=rendered_lines,
  )
```

## 新規 Replay 選択モジュール

```python
"""Phase 164 R5-R2: select a proof replay, never render text here.

All selected replays must pass through the same presentation and renderer.
Existing specialized proof construction is preserved in this phase.
"""
from toda_group_result_proof_replay import build_toda_group_result_proof_replay


def build_phase164_r5_r2_common_replay(n: int, k: int, group_result, max_depth: int, mode: str):
    """Select an existing proof root; return replay without Markdown or Web views."""
    if mode == "narrative" and n == 3 and k == 2:
        from phase164_r5_web_registry_connection import build_phase164_r5_web_pi5_3_proof

        replay, _ = build_phase164_r5_web_pi5_3_proof(max_depth=max_depth)
        return replay

    if mode == "narrative" and k == 1 and n in (4, 5):
        from toda_calculation_facade import build_standard_toda_report
        from toda_stable_eta_proof_replay import build_toda_stable_eta_proof_replay

        base_report = build_standard_toda_report(n=3, k=1)
        if len(base_report.candidates) != 1:
            raise ValueError("stable eta proof requires one base group result")
        base_result = base_report.candidates[0].source_candidate.group_result
        derived = build_toda_stable_eta_proof_replay(
            group_result, base_result, max_depth=max(3, max_depth)
        )
        return derived.replay

    return build_toda_group_result_proof_replay(group_result, max_depth=max_depth)
```

## 新規局所テスト

```python
"""R5-R2 focuses on a single common display path, not proof content quality."""
import ast
from pathlib import Path
from types import SimpleNamespace

import pytest

import phase164_r5_r2_common_replay as selector
import web_group_proof as web


def test_one_public_web_builder_has_one_common_narrative_renderer():
    source = Path(web.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    builders = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                and node.name == "build_standard_web_group_proof_view"]
    assert len(builders) == 1
    body = ast.get_source_segment(source, builders[0])
    assert body.count("render_toda_group_proof_narrative_markdown(presentation)") == 1
    assert body.count("build_toda_group_proof_presentation(replay)") == 1
    assert "build_phase162_r4_b3_web_common_display_view" not in body
    assert "build_phase164_r5_web_pi5_3_proof" not in body
    assert "build_phase164_r5_r2_common_replay" in body


def test_standard_selector_preserves_repository_replay(monkeypatch):
    sentinel = object()
    monkeypatch.setattr(selector, "build_toda_group_result_proof_replay",
                        lambda result, max_depth: (result, max_depth))
    assert selector.build_phase164_r5_r2_common_replay(6, 3, sentinel, 2, "narrative") == (sentinel, 2)
    assert selector.build_phase164_r5_r2_common_replay(3, 2, sentinel, 0, "trace") == (sentinel, 0)


def test_source_selection_requires_no_markdown_for_ordinary_groups(monkeypatch):
    calls = []
    monkeypatch.setattr(selector, "build_toda_group_result_proof_replay",
                        lambda result, max_depth: calls.append((result, max_depth)) or result)
    for n in range(2, 16):
        for k in range(8):
            if (n, k) in ((3, 2), (4, 1), (5, 1)):
                continue
            item = (n, k)
            assert selector.build_phase164_r5_r2_common_replay(
                n, k, item, 2, "narrative"
            ) == item
    assert len(calls) == 109


def test_legacy_special_web_view_is_not_reachable():
    source = Path(web.__file__).read_text(encoding="utf-8")
    block = source[source.index("def build_standard_web_group_proof_view("):]
    assert "_phase158_baseline_render_toda_group_proof_narrative_markdown" not in block


def test_pi53_common_narrative_is_renderable():
    view = web.build_standard_web_group_proof_view(3, 2, 2, "narrative")
    assert view.phase == "164 R5"
    assert view.rendered_lines
    assert view.mode == "narrative"


@pytest.mark.parametrize("n,k", [(4, 1), (5, 1), (4, 2), (6, 3)])
def test_representative_group_uses_single_view(n, k):
    view = web.build_standard_web_group_proof_view(n, k, 2, "narrative")
    assert view.rendered_lines
    assert view.n == n and view.k == k
    assert view.mode == "narrative"
```

## 変更適用スクリプト

```python
"""Fail-closed replacement of the sole public Web group builder."""
import ast
from pathlib import Path
import shutil


def main() -> None:
    bundle = Path(__file__).resolve().parent
    project = bundle.parent
    target = project / "web_group_proof.py"
    before = target.read_text(encoding="utf-8-sig")
    tree = ast.parse(before)
    found = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name == "build_standard_web_group_proof_view"]
    if len(found) != 1:
        raise ValueError("Expected exactly one public Web group proof builder")
    original = found[0]
    previous = ast.get_source_segment(before, original)
    if "phase164_r5_r2_common_replay" in previous:
        print("R5-R2 Web group builder already installed")
        return
    if "phase164_r5_web_registry_connection" not in previous:
        raise ValueError("R5-R1 baseline missing: refusing to overwrite unexpected code")
    replacement = (bundle / "replacement_web_function.txt").read_text(encoding="utf-8")
    ast.parse(replacement)
    lines = before.splitlines(keepends=True)
    start = sum(len(line) for line in lines[:original.lineno - 1])
    end = sum(len(line) for line in lines[:original.end_lineno])
    after = before[:start] + replacement.rstrip() + "\n" + before[end:]
    ast.parse(after)
    backup = project / "web_group_proof.phase164_r5_r2_backup.py"
    if not backup.exists():
        backup.write_text(before, encoding="utf-8")
    target.write_text(after, encoding="utf-8")
    print("Updated unified Web group proof builder; backup:", backup.name)


if __name__ == "__main__":
    main()
```

## 112群監査スクリプト

```python
"""Actual 112-target Web Narrative route audit; never modifies proof data."""
import json
from pathlib import Path

from web_group_proof import build_standard_web_group_proof_view
from web_group_query import build_standard_web_group_query_view


def main():
    output = Path("phase164_r5_r2_output")
    output.mkdir(exist_ok=True)
    results = []
    for n in range(2, 16):
        for k in range(8):
            item = {"n": n, "k": k}
            try:
                query = build_standard_web_group_query_view(n, k)
                if not query.proof_available:
                    item["status"] = "NO_PROOF_AVAILABLE"
                else:
                    view = build_standard_web_group_proof_view(n, k, 2, "narrative")
                    if not view.rendered_lines or view.mode != "narrative":
                        raise ValueError("common Narrative produced no lines")
                    if not view.conclusion_latex:
                        raise ValueError("missing proof conclusion")
                    item["status"] = "COMMON_VIEW_OK"
                    item["phase"] = view.phase
            except Exception as error:
                item["status"] = "ERROR"
                item["error"] = type(error).__name__ + ": " + str(error)
            results.append(item)
            print("pi", n + k, "^", n, item["status"], flush=True)
    counts = {name: sum(row["status"] == name for row in results)
              for name in ("COMMON_VIEW_OK", "NO_PROOF_AVAILABLE", "ERROR")}
    report = {"phase": "164 R5-R2", "targets": 112, "counts": counts,
              "all_available_proofs_use_common_view": counts["ERROR"] == 0,
              "full_pytest_run": False, "results": results}
    (output / "report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "results"}, ensure_ascii=False, indent=2))
    if counts["ERROR"]:
        raise SystemExit("112-target common display audit failed; see report.json")


if __name__ == "__main__":
    main()
```

## Windows 実行スクリプト

```powershell
$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project
$Source = Join-Path $PSScriptRoot 'phase164_r5_r2_common_replay.py'
$Target = Join-Path $Project 'phase164_r5_r2_common_replay.py'
Copy-Item $Source $Target -Force
$TestSource = Join-Path $PSScriptRoot 'tests\test_phase164_r5_r2_unified_web_display.py'
$TestTarget = Join-Path $Project 'tests\test_phase164_r5_r2_unified_web_display.py'
Copy-Item $TestSource $TestTarget -Force
python -B (Join-Path $PSScriptRoot 'apply_patch.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R2 patch rejected the current source' }
python -B -m pytest -q tests/test_phase164_r5_r2_unified_web_display.py tests/test_phase164_r5_r1_common_renderer.py
if ($LASTEXITCODE -ne 0) { throw 'R5-R2 targeted pytest failed' }
python -B (Join-Path $PSScriptRoot 'sweep_112.py')
if ($LASTEXITCODE -ne 0) { throw 'R5-R2 112-target sweep failed' }
Write-Host 'Phase 164 R5-R2 single common Web renderer route installed. Full pytest NOT run.'
```

## 実行する pytest

`python -B -m pytest -q tests/test_phase164_r5_r2_unified_web_display.py tests/test_phase164_r5_r1_common_renderer.py`

## 完了条件

112対象のうち証明が存在する対象の表示が共通経路で成功し、旧専用 Web View が呼び出されないこと。`report.json` の `ERROR` が 0 であること。証明がない対象は `NO_PROOF_AVAILABLE` として明示する。

## 次の段階との境界

旧モジュールの削除・本文品質改善・全体 pytest は今回は実施しない。
