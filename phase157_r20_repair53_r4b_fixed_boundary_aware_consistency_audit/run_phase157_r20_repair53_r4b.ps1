$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r4b - fixed-boundary-aware consistency audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "Test changes: none"
Write-Host "pytest: not run"
Write-Host "Repository-wide pytest: not run"
Write-Host ""

python ".\phase157_r20_repair53_r4b_fixed_boundary_aware_consistency_audit\audit_phase157_r20_repair53_r4b.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r4b audit execution failed."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r4b audit completed"
Write-Host "Production code changes: none"
Write-Host "Test changes: none"
Write-Host "pytest: not run"
Write-Host "=============================================================="
