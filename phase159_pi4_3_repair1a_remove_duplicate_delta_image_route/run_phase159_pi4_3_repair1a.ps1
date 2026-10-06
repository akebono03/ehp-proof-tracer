$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair1a"
Write-Host "Remove duplicate legacy Delta-image route"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Apply repair1a"
python "$PackageRoot\apply_phase159_pi4_3_repair1a.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair1a apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/4] Compile changed module and focused test"
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
Write-Host "[4/4] Verify unique direct provenance"
python "$PackageRoot\audit_phase159_pi4_3_repair1a.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair1a provenance audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 repair1a complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
