$ErrorActionPreference = "Stop"
$root = (Get-Location).Path
$package = Split-Path -Parent $MyInvocation.MyCommand.Path
if (!(Test-Path (Join-Path $root "proof.py"))) { throw "Run this script from the repository root" }
python -B (Join-Path $package "apply.py")
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest (Join-Path $package "test_r10.py") -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R10 focused tests completed. Full suite not run."
