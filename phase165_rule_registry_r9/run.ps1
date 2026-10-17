$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase165_rule_registry_r9.audit
    if ($LASTEXITCODE -ne 0) { throw 'R9 audit failed' }
    python -m pytest -q phase165_rule_registry_r9/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R9 targeted tests failed' }
    Write-Host 'R9 audit passed; full pytest NOT run.'
} finally {
    Pop-Location
}
