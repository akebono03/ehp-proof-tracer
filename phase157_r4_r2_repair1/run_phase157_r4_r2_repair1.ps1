$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R4-R2 repair1 - tracked-reference test contract"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""
Write-Host "Production code changes: none"
Write-Host ""

python "$PackageDir\apply_phase157_r4_r2_repair1.py"

Write-Host ""
Write-Host "Focused pytest only:"
python -m pytest `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase157_r4_r2_boundary_catalog.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  tests/test_phase157_r3_repair3_recursive_internal_recovery.py `
  tests/test_phase153_r5_reference_selection.py `
  tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py `
  -q

Write-Host ""
Write-Host "Phase157-R4-R2 repair1 complete."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."
