$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r37_page7_source_normalization\tests\test_review.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r37_page7_source_normalization.review `
  --source ".\phase163_r4_r36_output\Toda_01_corrected.tex" `
  --ledger ".\phase163_r4_r36_output\page_ledger.json" `
  --output ".\phase163_r4_r37_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R37 source and normalization separately recorded. Full suite not run."
