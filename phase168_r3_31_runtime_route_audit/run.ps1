$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q (Join-Path $package "tests\test_phase168_r3_31_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "Audit unit tests failed" }
    python (Join-Path $package "audit.py")
    if ($LASTEXITCODE -ne 0) { throw "Runtime route audit failed; read output JSON" }
    Write-Host "R3-31 audit only; source files unchanged; full pytest NOT run."
}
finally { Pop-Location }
