$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q ".\phase163_r1d_registry_identity\tests\test_audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B ".\phase163_r1d_registry_identity\audit.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "Reports: $root\phase163_r1d_output"
