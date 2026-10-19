$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3_permission_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3 production boundary audit failed' }
    python -m pytest -q phase166_r3_permission_audit/test_audit.py tests/test_phase165_r2_registry_lookup.py
    if ($LASTEXITCODE -ne 0) { throw 'R3 targeted tests failed' }
    Write-Host 'R3 audit completed; no production changes; full pytest NOT run.'
} finally { Pop-Location }
