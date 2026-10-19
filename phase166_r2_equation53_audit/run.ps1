$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Push-Location $Root
try {
    python -m phase166_r2_equation53_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2 (5.3) audit failed' }
    python -m pytest -q phase166_r2_equation53_audit/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2 (5.3) targeted pytest failed' }
    Write-Host 'R2 (5.3) read-only audit PASS; full pytest NOT run.'
} finally {
    Pop-Location
}
