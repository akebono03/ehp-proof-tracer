$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r55_nk_only_goal.py')) { throw 'Run in project root.' }
python .\phase166_r3af_goal_source\install.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AF install failed' }
python -m pytest -q phase166_r3af_goal_source/tests/test_r3af.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AF limited tests failed' }
Write-Host 'R3-AF limited tests complete; full pytest NOT run.'
