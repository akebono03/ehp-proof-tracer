$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Set-Location $Root
if (-not (Test-Path '.\phase165_r9_production_wiring.py')) { throw 'Run from an EHP Proof Tracer project root' }
python -m phase166_r3_order_audit.audit
if ($LASTEXITCODE -ne 0) { throw 'R3 inventory failed' }
python -m pytest -q phase166_r3_order_audit/test_audit.py
if ($LASTEXITCODE -ne 0) { throw 'R3 focused tests failed' }
Write-Host 'READ-ONLY audit completed. No production changes; full pytest NOT run.'
