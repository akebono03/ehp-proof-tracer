$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r4a - pi15^8 post-remap Reference consistency audit"
Write-Host "=============================================================="
Write-Host "Production code changes: none"
Write-Host "pytest: not run"
Write-Host "Repository-wide pytest: not run"
Write-Host ""

python ".\phase157_r20_repair53_r4a_pi15_post_remap_reference_consistency_audit\audit_phase157_r20_repair53_r4.py"

if ($LASTEXITCODE -ne 0) {
  throw "repair53-r4 audit detected a hard consistency defect."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase157-R20 repair53-r4a audit completed"
Write-Host "Production code changes: none"
Write-Host "pytest: not run"
Write-Host "=============================================================="
