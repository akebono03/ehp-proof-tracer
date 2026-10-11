$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r32_page6_alignment\tests\test_align.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r32_page6_alignment.align `
  --source ".\phase163_r4_r31_output\Toda_01_corrected.tex" `
  --ledger ".\phase163_r4_r31_output\page_ledger.json" `
  --output ".\phase163_r4_r32_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R32 partial page-6 review complete. Full suite not run."
