$ErrorActionPreference = "Stop"
$root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $root
python -B -m pytest -q ".\phase163_r4_r33_page6_alignment\tests\test_align.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -B -m phase163_r4_r33_page6_alignment.align `
  --source ".\phase163_r4_r32_output\Toda_01_corrected.tex" `
  --ledger ".\phase163_r4_r32_output\page_ledger.json" `
  --output ".\phase163_r4_r33_output"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Host "R4-R33 page-six partial original alignment complete. Full suite not run."
