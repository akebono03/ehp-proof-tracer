$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r36_page7_review\tests\test_review.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r36_page7_review.review `
  --source ".\phase163_r4_r35_output\Toda_01_corrected.tex" `
  --ledger ".\phase163_r4_r35_output\page_ledger.json" `
  --output ".\phase163_r4_r36_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R36 printed page 7 partial review complete. Full suite not run."
