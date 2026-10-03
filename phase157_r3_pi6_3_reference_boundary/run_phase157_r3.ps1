$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R3 - pi_6^3 fixed-statement Reference boundary"
Write-Host "=============================================================="

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = (Get-Location).Path

Write-Host "Repository root: $RepositoryRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageRoot\apply_phase157_r3.py"

Write-Host ""
Write-Host "Focused pytest only:"
python -m pytest `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase157_r3_pi6_3_reference_boundary.py `
  tests/test_phase153_r5_reference_selection.py `
  tests/test_phase156_r5_repair9_test_contract_after_boundary_collapse.py `
  -q

Write-Host ""
Write-Host "Phase157-R3 focused verification complete."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."
