$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python -m pytest -q '.\phase168_r2_12_active_route_audit\tests\test_audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'Limited audit self-tests failed' }
    python '.\phase168_r2_12_active_route_audit\audit.py'
    if ($LASTEXITCODE -ne 0) { throw 'Runtime audit failed; inspect output files' }
} finally { Pop-Location }
