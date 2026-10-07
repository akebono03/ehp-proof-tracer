$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 map-property numbered-reasoning audit3"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/1] Audit semantic isomorphism ownership for the three unnumbered pairs"
python ".\phase159_r1_7c_r4_map_property_numbered_reasoning_audit3\audit_phase159_r1_7c_r4_map_property_numbered_reasoning_audit3.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit3 complete"
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
