$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair1"
Write-Host "Proposition 5.1 direct Delta-image provenance"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Apply repair1"
python "$PackageRoot\apply_phase159_pi4_3_repair1.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair1 apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/4] Compile changed/new modules"
python -m py_compile `
  ".\toda_delta_image_rules.py" `
  ".\toda_upstream_bootstrap.py" `
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
Write-Host "[4/4] Re-run corrected provenance route audit if present"
$AuditScript = ".\phase159_pi4_3_corrected_provenance_route_audit\audit_phase159_pi4_3_corrected_provenance_route.py"
if (Test-Path $AuditScript) {
  python $AuditScript
  if ($LASTEXITCODE -ne 0) {
    throw "post-repair provenance audit failed with exit code $LASTEXITCODE"
  }
}
else {
  Write-Host "Previous corrected provenance audit package not found; skipped."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 repair1 complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
