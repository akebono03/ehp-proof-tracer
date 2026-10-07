$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 map-property dearu source-route audit2"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/1] Classify source routes for public map-property dearu lines"
python ".\phase159_r1_7c_r4_map_property_dearu_audit2\audit_phase159_r1_7c_r4_map_property_dearu_audit2.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit2 complete"
Write-Host "Production code changes: none"
Write-Host "Test code changes: none"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
