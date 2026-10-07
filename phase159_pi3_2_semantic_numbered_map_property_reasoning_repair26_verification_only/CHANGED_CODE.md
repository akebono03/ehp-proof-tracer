# Phase 159 repair26 verification only

## 変更対象

production:
- 変更なし

tests:
- 変更なし

追加する確認用ファイル:
- `verify_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair26.py`
- `run_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair26.ps1`

## 原因

repair25 の focused pytest は 19件すべて PASS した。

失敗したのは runner の `[4/4]` のみで、PowerShell here-string 内に直接埋め込んだ
日本語文字列 `## 証明` が Windows PowerShell 側で文字化けし、Python に渡る時点で

```text
marker = "## ????
```

のように壊れたため、`SyntaxError: unterminated string literal` になった。

production の semantic comparison（意味比較）には関係しない。

## 修正

PowerShell から Python ソースを標準入力で渡すのをやめる。

UTF-8 の独立 Python ファイル:

`verify_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair26.py`

を直接実行する。

## 確認用 Python 全文

```python
from toda_calculation_facade import (
  build_standard_toda_report,
)
from toda_group_proof_narrative_renderer import (
  render_toda_group_proof_narrative_markdown,
)
from toda_group_proof_presentation import (
  build_toda_group_proof_presentation,
)
from toda_group_result_proof_replay import (
  build_toda_group_result_proof_replay,
)


def main() -> int:
  report = build_standard_toda_report(
    n=2,
    k=1,
  )
  group_result = (
    report.candidates[0]
    .source_candidate.group_result
  )
  replay = build_toda_group_result_proof_replay(
    group_result,
    max_depth=2,
  )
  presentation = build_toda_group_proof_presentation(
    replay
  )
  rendered = render_toda_group_proof_narrative_markdown(
    presentation
  )

  marker = "## 証明"
  marker_index = rendered.find(
    marker
  )

  if marker_index < 0:
    raise RuntimeError(
      "proof marker not found"
    )

  proof = rendered[
    marker_index:
  ]

  required_fragments = (
    "完全性より,",
    (
      r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
      r"\quad\text{は単射}. \qquad (1)"
    ),
    (
      r"H: \pi_{3}^{2} \to \pi_{3}^{3}"
      r"\quad\text{は全射}. \qquad (2)"
    ),
    (
      r"(1), (2) より, "
      r"$H: \pi_{3}^{2} \to \pi_{3}^{3}$ は同型."
    ),
  )

  missing = tuple(
    fragment
    for fragment in required_fragments
    if fragment not in proof
  )

  if missing:
    raise AssertionError(
      "expected pi_3^2 public narrative fragments are missing: "
      + repr(
        missing
      )
    )

  print(
    proof
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(
    main()
  )

```

## PowerShell runner 全文

```powershell
param()

$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 repair26 verification only"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "[1/2] Run focused regression tests"
python -m pytest -q `
  ".\tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py" `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"

if ($LASTEXITCODE -ne 0) {
  throw "focused pytest failed"
}

Write-Host ""
Write-Host "[2/2] Render and verify pi_3^2 public narrative"
python `
  ".\phase159_pi3_2_semantic_numbered_map_property_reasoning_repair26_verification_only\verify_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair26.py"

if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 verification failed"
}

Write-Host ""
Write-Host "Verification complete."
Write-Host "No production files were modified."
Write-Host "Repository-wide pytest was intentionally NOT run."

```

## 実行する pytest

```powershell
python -m pytest -q `
  ".\tests\test_phase159_pi3_2_semantic_numbered_map_property_reasoning_repair25.py" `
  ".\tests\test_phase159_r1_7c_r4_map_property_numbered_reasoning_repair1.py" `
  ".\tests\test_phase159_r1_2_pi3_2_narrative_repair.py" `
  ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"
```

## 完了条件

- focused pytest が再び全 PASS。
- pi_3^2 public Narrative を正常に表示できる。
- `完全性より,` が確認できる。
- H の単射 `(1)` と全射 `(2)` が確認できる。
- `(1), (2) より` の同型結論が確認できる。

## 次 Phase との境界

これは verification-only（確認のみ）。

- production は変更しない。
- tests は変更しない。
- semantic model は変更しない。
- 全体 pytest は実行しない。
