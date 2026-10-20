$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m phase166_r3t_provenance.audit
    if ($LASTEXITCODE -ne 0) { throw 'R3-T provenance audit failed.' }
    python -m pytest -q phase166_r3t_provenance/test_audit.py
    if ($LASTEXITCODE -ne 0) { throw 'R3-T provenance targeted tests failed.' }
    Write-Host 'R3-T provenance audit finished; production untouched; full pytest NOT run.'
} finally {
    Pop-Location
}
