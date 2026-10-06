$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair1c"
Write-Host "Prop56 direct Proposition 5.1 dependency"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/5] Apply repair1c"
python "$PackageRoot\apply_phase159_pi4_3_repair1c.py"
if ($LASTEXITCODE -ne 0) {
  throw "repair1c apply failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/5] Compile changed/new files"
python -m py_compile `
  ".\toda_prop56_zero_bootstrap.py" `
  ".\tests\test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py"
if ($LASTEXITCODE -ne 0) {
  throw "py_compile failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/5] Run repair1c focused regression"
python -m pytest `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase55_prop51_integration.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[4/5] Verify standard production repository builds"
python -c "from standard_production_repository import build_standard_production_proof_repository; r=build_standard_production_proof_repository(); print('STANDARD_PRODUCTION_REPOSITORY=PASS' if r is not None else 'STANDARD_PRODUCTION_REPOSITORY=NONE')"
if ($LASTEXITCODE -ne 0) {
  throw "standard production repository build failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[5/5] Re-run post-repair1 Narrative ownership audit"
$AuditScript = ".\phase159_pi4_3_repair1_post_narrative_ownership_audit\audit_phase159_pi4_3_post_repair1_narrative_ownership.py"
if (Test-Path $AuditScript) {
  python $AuditScript
  if ($LASTEXITCODE -ne 0) {
    throw "Narrative ownership audit failed with exit code $LASTEXITCODE"
  }
}
else {
  Write-Host "Previous Narrative ownership audit package not found; skipped."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 159 pi_4^3 repair1c complete"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
