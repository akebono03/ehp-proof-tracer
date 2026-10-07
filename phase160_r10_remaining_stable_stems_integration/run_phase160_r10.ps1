$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 160-R10 Remaining stable stems integration"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/2] Apply Phase 160-R10"
python "$PackageRoot\apply_phase160_r10.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run focused tests only"
python -m pytest -q `
  "tests/test_phase160_remaining_stable_production.py" `
  "tests/test_phase160_remaining_stable_public_narrative.py" `
  "tests/test_phase160_generic_finite_cyclic_transport.py" `
  "tests/test_phase160_k2_generic_transport_connection.py" `
  "tests/test_phase160_k2_public_narrative.py" `
  "tests/test_phase160_generic_stable_public_narrative.py" `
  "tests/test_phase65_nu5_stable_transport.py" `
  "tests/test_phase68_prop58_integration.py" `
  "tests/test_phase70_prop59_integration.py" `
  "tests/test_phase73_pi_n_plus_6_n_nu_squared.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 160-R10 focused verification completed."
Write-Host "No full test suite was run."
