$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$bundle = Join-Path $root 'phase166_r3ai_112_goal_audit'
if (-not (Test-Path (Join-Path $root 'phase166_r3af_goal_adapter.py'))) { throw 'Run in the repository root.' }
$env:PYTHONPATH = $root
python (Join-Path $bundle 'audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
python -m pytest -q (Join-Path $bundle 'tests/test_goal_audit.py')
if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
Write-Host 'Targeted pytest PASS; full pytest NOT run.'
