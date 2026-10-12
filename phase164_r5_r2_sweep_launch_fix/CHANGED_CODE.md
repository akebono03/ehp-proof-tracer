# Phase 164 R5-R2 — 起動修正

変更ファイルは `run.ps1` のみです。既存 Python 関数・クラス・import・テストには変更ありません。

## run.ps1 全文

```powershell
$ErrorActionPreference = 'Stop'
$Project = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Project

$Required = @(
  'web_group_proof.py',
  'phase164_r5_r2_common_replay.py',
  'phase164_r5_r2_unified_web_display\sweep_112.py'
)
foreach ($RelativePath in $Required) {
  if (-not (Test-Path (Join-Path $Project $RelativePath))) {
    throw "Required file missing: $RelativePath"
  }
}

# -m includes the project root on sys.path, unlike running a nested script by path.
python -B -m phase164_r5_r2_unified_web_display.sweep_112
if ($LASTEXITCODE -ne 0) {
  throw 'R5-R2 112-target sweep failed; inspect phase164_r5_r2_output\report.json'
}
Write-Host 'Phase 164 R5-R2 112-target sweep completed. Full pytest NOT run.'
```

## 実行対象

既存の `phase164_r5_r2_unified_web_display/sweep_112.py` の `main()` をモジュール実行します。元の `run.ps1` にあったパス指定による実行を、`python -B -m phase164_r5_r2_unified_web_display.sweep_112` に変更します。既存の14件の対象テストは成功済みなので再実行しません。

## 完了条件

112件を走査して `phase164_r5_r2_output/report.json` を生成し、`ERROR` が0件であることです。失敗した場合は report を確認します。全体 pytest は行いません。
