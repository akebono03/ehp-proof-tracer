$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -m pytest -q '.\phase165_r6_8_3_retire_legacy\tests\test_retirement_guard.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python '.\phase165_r6_8_3_retire_legacy\retire.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R6-8(3) retirement applied. Full pytest NOT run. R6-9 NOT started.'
