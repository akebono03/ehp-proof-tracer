$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q '.\phase163_r4_r19_equation_audit\tests\test_audit.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r19_equation_audit.audit --source '.\phase163_r4_r19_equation_audit\Toda_01.tex' --output '.\phase163_r4_r19_output'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R19 equation audit complete. No production code changed; full suite not run.'
