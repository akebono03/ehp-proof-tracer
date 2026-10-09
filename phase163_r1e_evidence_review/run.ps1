$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$env:PYTHONPATH = $PSScriptRoot
python -B -m pytest -q (Join-Path $PSScriptRoot 'tests\test_audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B (Join-Path $PSScriptRoot 'audit.py')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Reports: $root\phase163_r1e_output"
