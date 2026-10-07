$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 display-math period audit1"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/1] Audit public Narrative display-math periods"
python ".\phase159_r1_7c_r4_display_math_period_audit1\audit_phase159_r1_7c_r4_display_math_period_audit1.py"
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
