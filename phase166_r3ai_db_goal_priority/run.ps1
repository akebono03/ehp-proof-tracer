$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$bundle = Join-Path $root 'phase166_r3ai_db_goal_priority'
if (-not (Test-Path (Join-Path $root 'phase166_r3af_goal_adapter.py'))) { throw 'Run in repository root' }
python (Join-Path $bundle 'apply.py')
if ($LASTEXITCODE -ne 0) { throw 'patch failed' }
python -m pytest -q (Join-Path $bundle 'tests/test_r3ai.py') (Join-Path $root 'phase166_r3af_test_fixture_fix/test_r3af.py')
if ($LASTEXITCODE -ne 0) { throw 'targeted pytest failed' }
Write-Host 'Targeted pytest PASS; full pytest NOT run.'
