$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    if (!(Test-Path '.\phase166_r2_typed53\audit.py')) {
        throw 'Previous R2 typed (5.3) audit is required.'
    }
    python -m phase166_r2_assertion_binding.audit
    if ($LASTEXITCODE -ne 0) { throw 'R2 binding audit failed' }
    python -m pytest -q phase166_r2_assertion_binding/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R2 binding targeted pytest failed' }
    Write-Host 'R2 candidate binding PASS; production unchanged; full pytest NOT run.'
} finally {
    Pop-Location
}
