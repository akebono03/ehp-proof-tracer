$ErrorActionPreference = 'Stop'
if (-not (Test-Path '.\phase165_r52_r9_shared_math.py')) { throw 'Run from project root' }
python -m phase166_r3ad_stable_transport_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'Audit failed' }
python -m pytest -q phase166_r3ad_stable_transport_audit/test_r3ad.py
if ($LASTEXITCODE -ne 0) { throw 'Focused test failed' }
Write-Host 'R3-AD read-only audit finished; full pytest NOT run.'
