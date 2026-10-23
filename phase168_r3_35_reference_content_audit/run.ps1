$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python -m pytest -q (Join-Path $package "tests\test_r3_35_static_contract.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-35 limited tests failed" }
    python (Join-Path $package "audit.py")
    if ($LASTEXITCODE -ne 0) { throw "R3-35 reference audit failed" }
    Write-Host "R3-35 audit only. Source unchanged; full pytest NOT run."
}
finally { Pop-Location }
