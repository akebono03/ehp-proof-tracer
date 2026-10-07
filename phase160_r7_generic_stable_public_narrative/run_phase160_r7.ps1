$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 160-R7 generic stable public Narrative"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/2] Apply Phase 160-R7"
python "$PackageRoot\apply_phase160_r7.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run focused tests only"
python -m pytest -q `
  "tests/test_phase160_generic_stable_public_narrative.py" `
  "tests/test_phase159_pi_nplus1_n_stable_transport.py" `
  "tests/test_phase160_k1_generic_transport_connection.py" `
  "tests/test_phase160_k7_generic_transport_connection.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 160-R7 focused verification completed."
Write-Host "No full test suite was run."
