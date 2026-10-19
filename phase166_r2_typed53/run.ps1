$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r2_typed53.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2 typed audit failed' }
    python -m pytest -q phase166_r2_typed53/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2 targeted pytest failed' }
    Write-Host 'R2 typed (5.3) audit PASS; production code unchanged; full pytest NOT run.'
} finally {
    Pop-Location
}
