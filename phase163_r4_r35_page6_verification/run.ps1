$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r35_page6_verification\tests\test_verify.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r35_page6_verification.verify `
  --source ".\phase163_r4_r34_output\Toda_01_corrected.tex" `
  --ledger ".\phase163_r4_r34_output\page_ledger.json" `
  --output ".\phase163_r4_r35_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R35 printed page 6 mathematical review complete. Full suite not run."
