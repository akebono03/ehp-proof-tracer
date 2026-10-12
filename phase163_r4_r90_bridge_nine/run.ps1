$ErrorActionPreference = "Stop"
$Project = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Project
python -m pytest -q ".\phase163_r4_r90_bridge_nine\tests\test_phase163_r4_r90_bridge_nine.py"
if ($LASTEXITCODE -ne 0) { throw "R90 targeted tests failed" }
python -m phase163_r4_r90_bridge_nine.phase163_r4_r90_bridge_nine
if ($LASTEXITCODE -ne 0) { throw "R90 bridge report failed" }
