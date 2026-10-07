$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - repair2g fix10j"
Write-Host "Corrected verification only"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Corrected pi_3^2 / pi_4^3 public Narrative audit"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix10j.py"
if ($LASTEXITCODE -ne 0) {
  throw "fix10j corrected audit failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/4] Run pi_3^2 Narrative contract"
python -m pytest `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "pi_3^2 Narrative contract failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/4] Run repair2g focused tests"
python -m pytest `
  tests/test_phase159_pi4_3_repair2g_reference_policy.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair2g focused tests failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[4/4] Run repair1 health checks"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair1 health checks failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "fix10j verification complete"
Write-Host "Production code changes: NONE"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
