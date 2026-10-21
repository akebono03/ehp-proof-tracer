$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r55_nk_only_goal.py')) { throw 'Run from the project repository root.' }
python -m phase166_r3ah_provenance_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3-AH audit failed' }
python -m pytest -q phase166_r3ah_provenance_audit/test_r3ah.py
if ($LASTEXITCODE -ne 0) { throw 'R3-AH focused tests failed' }
Write-Host 'R3-AH read-only audit completed. Full pytest NOT run.'
