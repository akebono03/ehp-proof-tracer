$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 159 R1-7c R4 generator canonicalization repair1 fix2"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "Repository root: $RepoRoot"
Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/5] Apply stale explicit-marker expectation repair"
python ".\phase159_r1_7c_r4_generator_canonicalization_repair1_fix2\apply_phase159_r1_7c_r4_generator_canonicalization_repair1_fix2.py"
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[2/5] Run current pi6^3 dependency/reference regression"
python -m pytest `
  ".\tests\test_phase157_r20_generic_dependency_rendering.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[3/5] Run repair1 focused regression"
python -m pytest `
  ".\tests\test_phase159_r1_7c_r4_generator_canonicalization_repair1.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[4/5] Run generic eta normalization regression"
python -m pytest `
  ".\tests\test_phase143_3_generic_eta_normalization.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "[5/5] Run Proposition 5.3 integration regression"
python -m pytest `
  ".\tests\test_phase59_prop53_integration.py" `
  -q
if ($LASTEXITCODE -ne 0) {
  exit $LASTEXITCODE
}

Write-Host ""
Write-Host "=============================================================="
Write-Host "Repair1 fix2 focused verification complete"
Write-Host "Full pytest was NOT run."
Write-Host "=============================================================="
