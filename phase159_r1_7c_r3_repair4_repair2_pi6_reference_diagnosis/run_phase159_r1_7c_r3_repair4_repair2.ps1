$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R3 repair4 repair2"
Write-Host "pi_6^3 Reference diagnosis only"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host ""

python `
  ".\phase159_r1_7c_r3_repair4_repair2_pi6_reference_diagnosis\audit_phase159_r1_7c_r3_repair4_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair4 repair2 audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Audit completed."
Write-Host "No repository files were modified."
Write-Host "Repository-wide pytest was intentionally NOT run."
