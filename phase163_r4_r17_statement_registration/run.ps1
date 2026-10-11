$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
$source = Join-Path $PSScriptRoot 'Toda_01.tex'
if (-not (Test-Path $source)) { throw 'Toda_01.tex not found in package' }
python -B -m pytest -q .\phase163_r4_r17_statement_registration\tests\test_register.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r17_statement_registration.register --source $source --output .\phase163_r4_r17_output
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'Phase 163 R4-R17 named statements registered. Full suite not run.'
