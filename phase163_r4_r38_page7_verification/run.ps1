$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r38_page7_verification\tests\test_verify.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r38_page7_verification.verify `
  --source ".\phase163_r4_r37_output\Toda_01_corrected.tex" `
  --ledger ".\phase163_r4_r37_output\page_ledger.json" `
  --normalization ".\phase163_r4_r37_output\source_normalization.json" `
  --output ".\phase163_r4_r38_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R38 mathematical comparison recorded. Full suite not run."
