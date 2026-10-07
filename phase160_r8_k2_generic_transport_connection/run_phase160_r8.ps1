$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 160-R8 k=2 generic stable transport connection"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/2] Apply Phase 160-R8"
python "$PackageRoot\apply_phase160_r8.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run focused tests only"
python -m pytest -q `
  "tests/test_phase160_generic_finite_cyclic_transport.py" `
  "tests/test_phase160_k2_generic_transport_connection.py" `
  "tests/test_phase59_prop53_integration.py" `
  "tests/test_phase100_prop56_midstream.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 160-R8 focused verification completed."
Write-Host "No full test suite was run."
