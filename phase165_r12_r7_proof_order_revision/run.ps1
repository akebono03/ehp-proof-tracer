$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONIOENCODING = "utf-8"
python (Join-Path $PSScriptRoot "install.py")
if ($LASTEXITCODE -ne 0) { throw "R12-R7 installation failed" }
python -m pytest -q (Join-Path $PSScriptRoot "tests")
if ($LASTEXITCODE -ne 0) { throw "R12-R7 targeted tests failed" }
Write-Output "R12-R7 targeted tests completed. Full pytest NOT run."
