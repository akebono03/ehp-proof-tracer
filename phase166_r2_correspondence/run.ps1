$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -m phase166_r2_correspondence.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2 audit failed' }
    python -m pytest -q phase166_r2_correspondence/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2 targeted tests failed' }
    Write-Host 'R2 correspondence candidate audit PASS; no production modification; full pytest NOT run.'
} finally {
    Pop-Location
}
