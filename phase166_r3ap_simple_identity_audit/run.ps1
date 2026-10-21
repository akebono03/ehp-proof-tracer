$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
Push-Location $root
try {
    python -m phase166_r3ap_simple_identity_audit.audit
    if ($LASTEXITCODE -ne 0) { throw 'Identity audit failed' }
    python -m pytest -q phase166_r3ap_simple_identity_audit/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'Targeted pytest failed' }
    Write-Host 'Read-only identity audit complete; full pytest NOT run.'
} finally {
    Pop-Location
}
