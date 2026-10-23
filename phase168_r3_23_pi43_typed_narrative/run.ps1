$ErrorActionPreference = "Stop"
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
$project = Split-Path -Parent $package
Push-Location $project
try {
    python (Join-Path $package "apply.py")
    if ($LASTEXITCODE -ne 0) { throw "Patch failed" }
    python -m pytest -q (Join-Path $package "tests/test_phase168_r3_23_pi43_typed.py")
    if ($LASTEXITCODE -ne 0) { throw "Limited pytest failed" }
    Write-Host "R3-23 limited tests completed; full suite NOT run."
}
finally { Pop-Location }
