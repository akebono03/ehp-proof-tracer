$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -m pytest -q '.\phase165_r6_10_dependency_audit\test_audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R6-10 audit unit tests failed. No retirement attempted.' }
python '.\phase165_r6_10_dependency_audit\audit.py'
if ($LASTEXITCODE -ne 0) { throw 'R6-10 dependency audit failed.' }
Write-Host 'R6-10 read-only audit complete. Full pytest NOT run.'
