$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase157-R2 — Literature Statement Boundary"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

python "$PackageRoot\apply_phase157_r2.py"

Write-Host ""
Write-Host "Focused pytest only:"
python -m pytest `
  tests/test_phase157_r2_literature_statement_boundary.py `
  tests/test_phase153_r5_reference_selection.py `
  -q

Write-Host ""
Write-Host "Phase157-R2 focused verification complete."
Write-Host "Repository-wide pytest is intentionally deferred to Phase157 closure."
