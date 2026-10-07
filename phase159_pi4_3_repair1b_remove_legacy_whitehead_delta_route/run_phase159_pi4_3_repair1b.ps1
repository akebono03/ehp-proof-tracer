$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair1b"
Write-Host "Remove legacy Whitehead Delta route"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Apply repair1b"
python "$PackageRoot\apply_phase159_pi4_3_repair1b.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair1b apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/4] Compile changed/new modules"
python -m py_compile `
  ".\toda_upstream_bootstrap.py" `
  ".\toda_delta_image_rules.py" `
  ".\tests\test_phase159_pi4_3_prop51_direct_delta_provenance.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/4] Run focused repair1 regression"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase50_pi4_3_exactness_bridge.py `
  tests/test_phase50_pi4_3_finite_cyclic.py `
  tests/test_phase52_delta_direct_bridge.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[4/4] Verify direct-only Phase 50 provenance"
python "$PackageRoot\audit_phase159_pi4_3_repair1b.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair1b provenance audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 repair1b complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
