$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 158-R1 - Narrative Public Contract Inventory"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Resolve-Path (Join-Path $PackageDir "..")).Path

Set-Location $RepoRoot

Write-Host "[1/3] Focused helper tests"
python -m pytest `
  ".\phase158_r1_narrative_public_contract_inventory\test_phase158_r1_audit_helpers.py" `
  -q

Write-Host "[2/3] 112-group public-contract inventory"
python `
  ".\phase158_r1_narrative_public_contract_inventory\audit_phase158_r1.py"

Write-Host "[3/3] Show summary"
Get-Content `
  ".\phase158_r1_narrative_public_contract_inventory\output\narrative_public_contract_summary.txt"

Write-Host "=============================================================="
Write-Host "Phase 158-R1 complete."
Write-Host "Production code changes: none"
Write-Host "Full repository pytest: NOT run in R1"
Write-Host "=============================================================="
