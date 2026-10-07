$ErrorActionPreference = "Stop"

$PackageRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageRoot

Write-Host "=============================================================="
Write-Host "Phase 160-R9 k=2 public Narrative connection"
Write-Host "=============================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Set-Location $RepoRoot

Write-Host "[1/2] Apply Phase 160-R9"
python "$PackageRoot\apply_phase160_r9.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/2] Run focused tests only"
python -m pytest -q `
  "tests/test_phase160_k2_public_narrative.py" `
  "tests/test_phase160_generic_stable_public_narrative.py" `
  "tests/test_phase159_pi_nplus1_n_stable_transport.py" `
  "tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "Phase 160-R9 focused verification completed."
Write-Host "No full test suite was run."
