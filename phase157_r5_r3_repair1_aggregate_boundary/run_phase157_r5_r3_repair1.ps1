$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157-R5-R3 repair1 - aggregate boundary correction"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageDir\apply_phase157_r5_r3_repair1.py"

Write-Host ""
Write-Host "Focused lightweight pytest only:"

python -m pytest `
  tests/test_phase157_r5_r3_boundary_catalog_expansion.py `
  tests/test_phase157_r4_r2_boundary_catalog.py `
  tests/test_phase157_r2_literature_statement_boundary.py `
  -q

Write-Host ""
Write-Host "Phase157-R5-R3 repair1 focused verification complete."
Write-Host "112-group replay is not rerun in this repair."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."
