$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 160-R4 generic finite-cyclic stable transport"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/2] Apply Phase 160-R4"
python "$PackageRoot\apply_phase160_r4.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run focused tests only"
python -m pytest -q `
  "tests/test_phase160_stable_target_semantics.py" `
  "tests/test_phase160_canonical_toda45_specialization.py" `
  "tests/test_phase160_generic_finite_cyclic_transport.py" `
  "tests/test_phase53_finite_cyclic_transport.py" `
  "tests/test_phase75_sigma_stable_transport.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 160-R4 focused verification completed."
Write-Host "No full test suite was run."
