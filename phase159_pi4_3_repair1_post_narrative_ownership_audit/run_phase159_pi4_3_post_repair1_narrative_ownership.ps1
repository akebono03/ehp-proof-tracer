$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 post-repair1 Narrative ownership audit"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: none"
Write-Host "Existing test changes: none"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/2] Run depth=2 Narrative ownership audit"
python "$PackageRoot\audit_phase159_pi4_3_post_repair1_narrative_ownership.py"
if ($LASTEXITCODE -ne 0) {
  throw "Narrative ownership audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/2] Run focused pi_4^3 regression"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase50_pi4_3_exactness_bridge.py `
  tests/test_phase50_pi4_3_finite_cyclic.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "focused regression failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Audit complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
