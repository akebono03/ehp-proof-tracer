$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
$env:PYTHONPATH = $root
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUTF8 = "1"
Copy-Item -Path (Join-Path $PSScriptRoot "phase165_r12_r8_typed_source_connection.py") -Destination (Join-Path $root "phase165_r12_r8_typed_source_connection.py") -Force
python -m pytest -q (Join-Path $PSScriptRoot "tests")
if ($LASTEXITCODE -ne 0) { throw "R12-R8 focused tests failed" }
python (Join-Path $PSScriptRoot "audit.py")
if ($LASTEXITCODE -ne 0) { throw "R12-R8 source audit failed" }
Write-Output "R12-R8 typed source audit completed. Full pytest NOT run."
