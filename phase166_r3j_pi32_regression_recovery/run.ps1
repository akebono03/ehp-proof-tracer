$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
if (-not (Test-Path '.\phase165_r55_nk_only_goal.py')) { throw 'Run from the repository root.' }
$env:PYTHONPATH = if ($env:PYTHONPATH) { "$root;$env:PYTHONPATH" } else { $root }
python '.\phase166_r3j_pi32_regression_recovery\restore.py'
if ($LASTEXITCODE -ne 0) { throw 'Guarded restoration failed.' }
python -m pytest -q '.\phase166_r3j_pi32_regression_recovery\test_recovery.py' '.\test_phase165_r52_r9_shared_math.py'
if ($LASTEXITCODE -ne 0) { throw 'Focused regression tests failed.' }
Write-Host 'Regression recovery targeted PASS; full pytest NOT run.'
