$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase157 R11-R14 repair1 - partial apply recovery"
Write-Host "=============================================================="

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "Repository root: $RepoRoot"
Write-Host ""
Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "Applying repair1..."
python "$ScriptDir\apply_phase157_r11_r14_repair1.py"

if ($LASTEXITCODE -ne 0) {
  throw "R11-R14 repair1 patch failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Syntax checks:"
python -m py_compile `
  toda_group_proof_narrative_contribution_renderer.py `
  toda_group_proof_narrative_references.py `
  tests/test_phase157_r11_reference_reason_punctuation.py

if ($LASTEXITCODE -ne 0) {
  throw "R11-R14 repair1 syntax check failed with exit code $LASTEXITCODE"
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
  throw "R11-R14 repair1 focused pytest failed with exit code $LASTEXITCODE"
}

Write-Host ""
Write-Host "Current pi_6^3 narrative:"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=3,k=3); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"

Write-Host ""
Write-Host "Full repository pytest is NOT run here."
Write-Host "It remains deferred until Phase157 closure."
