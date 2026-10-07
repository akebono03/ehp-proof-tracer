$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 160-R6 repair2 direct sigma transport test"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/2] Apply Phase 160-R6 repair2"
python "$PackageRoot\apply_phase160_r6_repair2.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run focused tests only"
python -m pytest -q `
  "tests/test_phase160_generic_finite_cyclic_transport.py" `
  "tests/test_phase160_k7_generic_transport_connection.py" `
  "tests/test_phase100_prop515_upper_bootstrap.py" `
  "tests/test_phase109_20_sigma10_concrete_specialization.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 160-R6 repair2 focused verification completed."
Write-Host "No full test suite was run."
