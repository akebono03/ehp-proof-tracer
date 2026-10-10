$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r39_page8_review\tests\test_review.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r39_page8_review.review `
  --source ".\phase163_r4_r38_output\Toda_01_corrected.tex" `
  --ledger ".\phase163_r4_r38_output\page_ledger.json" `
  --output ".\phase163_r4_r39_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R39 source comparison complete; production unchanged; full suite not run."
