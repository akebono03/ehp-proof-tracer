$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 - pi_4^3 repair2g fix4v1"
Write-Host "(5.1) runtime catalog verification - import path repair"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host "Production code changes: NONE"
Write-Host "Existing test changes: NONE"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/5] Inspect active (5.1) fixed components"
python "$PackageRoot\audit_phase159_pi4_3_repair2g_fix4v1.py"
if ($LASTEXITCODE -ne 0) {
  throw "catalog verification failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[2/5] Run repair2g focused tests"
python -m pytest `
  tests/test_phase159_pi4_3_repair2g_reference_policy.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair2g focused tests failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[3/5] Run Phase159 repair1 health checks"
python -m pytest `
  tests/test_phase159_pi4_3_prop51_direct_delta_provenance.py `
  tests/test_phase159_pi4_3_repair1c_prop56_direct_prop51_dependency.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "repair1 health checks failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[4/5] Run low-dimensional contract checks"
python -m pytest `
  tests/test_phase49_probe.py `
  tests/test_phase49_low_dimensional_facts.py `
  tests/test_phase159_r1_2_pi3_2_narrative_repair.py `
  -q
if ($LASTEXITCODE -ne 0) {
  throw "low-dimensional contract checks failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "[5/5] Print pi_3^2 / pi_4^3 public Narrative"
$PreviousAudit = `
  "$RepositoryRoot\phase159_pi4_3_repair2g_fix2_boundary_catalog_completion\audit_phase159_pi4_3_repair2g.py"

if (Test-Path $PreviousAudit) {
  python $PreviousAudit
  if ($LASTEXITCODE -ne 0) {
    throw "repair2g verification audit failed with exit code $LASTEXITCODE"
  }
}
else {
  Write-Host "Previous repair2g audit script not found."
  Write-Host "Focused renderer tests are authoritative."
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "repair2g fix4v1 complete"
Write-Host "Production code changes: NONE"
Write-Host "Repository-wide pytest: NOT RUN"
Write-Host "=============================================================="
