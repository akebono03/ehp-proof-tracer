$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepositoryRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 159 pi_(n+1)^n stable transport repair1"
Write-Host "=============================================================="
Write-Host "Repository root: $RepositoryRoot"
Write-Host ""

Set-Location $RepositoryRoot

Write-Host "[1/4] Apply minimal production change and focused test"
python "$PackageRoot\apply_phase159_pi_nplus1_n_stable_transport_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/4] Run new focused tests"
python -m pytest -q tests/test_phase159_pi_nplus1_n_stable_transport.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/4] Run existing Toda (4.5) semantic test"
python -m pytest -q tests/test_phase153_r2_toda45_map_property_semantic.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/4] Run focused pi_4^3 regression tests"
python -m pytest -q `
  tests/test_phase159_pi4_3_trailing_premise_order.py `
  tests/test_phase159_pi4_3_exactness_surjectivity_unification.py `
  tests/test_phase159_pi4_3_repair2g_reference_policy.py
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Focused verification completed successfully."
Write-Host "Full suite is intentionally not run here; project policy runs it only at Phase end."
