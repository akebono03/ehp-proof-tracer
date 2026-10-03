$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R11-R11 repair3 - map-property classification"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "Applying repair3..."
python "$ScriptDir\apply_phase157_r11_r11_repair3.py"

if ($LASTEXITCODE -ne 0) {
  throw "R11-R11 repair3 patch failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Syntax checks:"
python -m py_compile `
  toda_proof_dependency.py `
  toda_group_proof_narrative_contribution_renderer.py `
  tests/test_phase157_r11_reference_reason_punctuation.py

if ($LASTEXITCODE -ne 0) {
  throw "R11-R11 repair3 syntax check failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Focused pytest:"
python -m pytest `
  tests/test_phase157_r11_reference_reason_punctuation.py `
  tests/test_phase157_r11_proof_body_relevance.py `
  tests/test_phase157_r5_r9_fixed_definition_body_suppression.py `
  tests/test_phase157_r5_r10_reference_proof_boundary_qed.py `
  tests/test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py `
  tests/test_phase93_dependency_role_classification.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "R11-R11 repair3 focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Production code changes in repair3:"
Write-Host "  toda_proof_dependency.py"
Write-Host "  toda_group_proof_narrative_contribution_renderer.py"
Write-Host ""
Write-Host "Full repository pytest is NOT run here."
Write-Host "It remains deferred until Phase157 closure."
