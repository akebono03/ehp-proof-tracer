$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q (Join-Path $package "tests\test_phase168_r3_32_audit.py")
    if ($LASTEXITCODE -ne 0) { throw "Focused audit tests failed" }
    python (Join-Path $package "audit.py")
    if ($LASTEXITCODE -ne 0) { throw "Audit reports REVIEW_REQUIRED; inspect generated output" }
    Write-Host "R3-32 audit only; repository source unchanged; full pytest NOT run."
}
finally { Pop-Location }
