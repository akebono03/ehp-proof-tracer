$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R5-R10 repair1 - Reference/Proof boundary + QED"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD

Write-Host ""
Write-Host "Applying idempotent repair patch..."
python "$PackageDir\apply_phase157_r5_r10.py"

Write-Host ""
Write-Host "Focused pytest:"
python -m pytest `
  tests/test_phase157_r5_r10_reference_proof_boundary_qed.py `
  tests/test_phase157_r5_r9_fixed_definition_body_suppression.py `
  tests/test_phase157_r5_r7_reference_definition_consequence_rendering.py `
  tests/test_phase132_9_web_group_proof_modes.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Phase157 R5-R10 repair1 focused checks passed."
Write-Host "Full repository pytest is intentionally NOT run here."
Write-Host "It will be run only at Phase157 closure."
