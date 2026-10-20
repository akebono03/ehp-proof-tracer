$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$env:PYTHONPATH = "$Root;$PSScriptRoot"
python ".\phase166_r3e_residual_audit\audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R3-E residual runtime audit failed' }
python -m pytest -q ".\phase166_r3e_residual_audit\test_audit.py"
if ($LASTEXITCODE -ne 0) { throw 'R3-E residual focused tests failed' }
Write-Host 'R3-E residual audit PASS; production code unchanged; full pytest NOT run.'
