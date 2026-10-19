$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Push-Location $root
try {
    python ".\phase166_r3_lookup_gate_fix\install.py"
    if ($LASTEXITCODE -ne 0) { throw 'R3 safe install failed' }
    python -m pytest -q '.\phase166_r3_lookup_gate_fix\test_gate.py' 'tests\test_phase165_r2_registry_lookup.py'
    if ($LASTEXITCODE -ne 0) { throw 'R3 targeted tests failed' }
    Write-Host 'R3 lookup gate targeted PASS; full pytest NOT run.'
} finally { Pop-Location }
