$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase166_r3af_goal_adapter.py')) { throw 'R3-AF adapter missing; execute at repository root' }
python -m phase166_r3ag_actual_search_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-AG audit failed' }
python -m pytest -q phase166_r3ag_actual_search_audit/test_r3ag.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AG focused tests failed' }
Write-Host 'R3-AG audit finished; no production files changed; no full pytest.'
