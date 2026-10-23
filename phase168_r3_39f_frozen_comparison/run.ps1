$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Push-Location $Project
try {
    python -m phase168_r3_39f_frozen_comparison.audit
    if ($LASTEXITCODE -ne 0) { throw "R3-39F audit failed" }
    python -m pytest -q ".\phase168_r3_39f_frozen_comparison\tests\test_audit.py"
    if ($LASTEXITCODE -ne 0) { throw "R3-39F focused tests failed" }
    Write-Host "R3-39F frozen comparison audit complete. Full suite NOT run."
}
finally {
    Pop-Location
}
