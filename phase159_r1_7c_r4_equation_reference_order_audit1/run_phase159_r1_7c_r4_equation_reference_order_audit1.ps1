$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 equation-reference order audit1"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/1] Audit forward equation-number references in public proof bodies"
python ".\phase159_r1_7c_r4_equation_reference_order_audit1\audit_phase159_r1_7c_r4_equation_reference_order_audit1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit1 complete"
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
