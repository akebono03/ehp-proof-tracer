$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R5-R4 repair2 - classifier-verified test rows"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageDir\apply_phase157_r5_r4_repair2.py"

Write-Host ""
Write-Host "Focused lightweight pytest only:"

python -m pytest `
  tests/test_phase157_r5_r4_generic_reference_selection.py `
  tests/test_phase157_r5_r3_boundary_catalog_expansion.py `
  tests/test_phase157_r4_r3_reference_selection_integration.py `
  tests/test_phase157_r4_r3_repair1_reference_retention.py `
  tests/test_phase157_r4_r2_boundary_catalog.py `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase153_r5_reference_selection.py `
  -q

Write-Host ""
Write-Host "Phase157-R5-R4 repair2 focused verification complete."
Write-Host "Production code was not changed by this repair."
Write-Host "112-group cross-audit remains deferred to Phase157-R5-R5."
Write-Host "Repository-wide pytest remains deferred to Phase157 closure."
