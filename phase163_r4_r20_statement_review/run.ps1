$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q '.\phase163_r4_r20_statement_review\tests\test_review.py'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r20_statement_review.review --source '.\phase163_r4_r19_equation_audit\Toda_01.tex' --output '.\phase163_r4_r20_output'
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host 'R4-R20 statement review completed; full suite not run.'
