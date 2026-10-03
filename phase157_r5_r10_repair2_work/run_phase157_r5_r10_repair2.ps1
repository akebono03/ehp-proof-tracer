$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R5-R10 repair2 - boundary test + web separator parser"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "Applying repair2 patch..."
python "$ScriptDir\apply_phase157_r5_r10_repair2.py"

Write-Host ""
Write-Host "Focused pytest:"
python -m pytest `
  tests/test_phase157_r5_r10_reference_proof_boundary_qed.py `
  tests/test_phase157_r5_r9_fixed_definition_body_suppression.py `
  tests/test_phase157_r5_r7_reference_definition_consequence_rendering.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Phase157 R5-R10 repair2 focused checks completed."
Write-Host "Full repository pytest is intentionally NOT run here."
Write-Host "It will be run only at Phase157 closure."
