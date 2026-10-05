$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R4-R3 repair2 - identity keys + lightweight tests"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageDir\apply_phase157_r4_r3_repair2.py"

Write-Host ""
Write-Host "Focused lightweight pytest only:"

python -m pytest `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase157_r4_r2_boundary_catalog.py `
  tests/test_phase157_r4_r3_reference_selection_integration.py `
  tests/test_phase157_r4_r3_repair1_reference_retention.py `
  tests/test_phase153_r5_reference_selection.py `
  -q

Write-Host ""
Write-Host "Phase157-R4-R3 repair2 lightweight verification complete."
Write-Host "No representative full-Narrative loop is run here."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."
