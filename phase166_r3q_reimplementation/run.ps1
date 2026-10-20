$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path (Join-Path $root 'phase165_r55_nk_only_goal.py'))) { throw 'Run from ehp_proof root.' }
python (Join-Path $PSScriptRoot 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'R3-Q patch failed' }
$backupFolder = Get-ChildItem (Join-Path $root 'phase166_r3q_reimplementation_backups') -Directory | Sort-Object Name -Descending | Select-Object -First 1
if ($null -eq $backupFolder) { throw 'Missing R3-Q backup' }
python -m pytest -q `
  phase166_r3q_reimplementation/tests/test_phase166_r3q_reimplementation.py `
  phase166_r3d_pi32_regression/tests/test_phase166_r3d_pi32_regression.py
if ($LASTEXITCODE -ne 0) {
  Copy-Item (Join-Path $backupFolder.FullName 'phase165_r55_nk_only_goal.py') (Join-Path $root 'phase165_r55_nk_only_goal.py') -Force
  throw 'R3-Q targeted regression failed: production module automatically restored from backup.'
}
Write-Host 'R3-Q limited PASS; full pytest NOT run.'
