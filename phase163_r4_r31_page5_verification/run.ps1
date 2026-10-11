$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r31_page5_verification\tests\test_verify.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r31_page5_verification.verify --source ".\phase163_r4_r30_output\Toda_01_corrected.tex" --ledger ".\phase163_r4_r30_output\page_ledger.json" --output ".\phase163_r4_r31_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R31 page-five mathematical content review complete. Full suite not run."
