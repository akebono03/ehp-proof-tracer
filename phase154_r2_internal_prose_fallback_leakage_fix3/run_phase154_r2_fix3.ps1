$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fix3 - Reference Marker Sentence Completion"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Assumption: Phase 154-R2 initial patch, Fixed1, and Fix2 are already applied."
Write-Host ""

Write-Host "Applying Fix3..."
python ".\phase154_r2_internal_prose_fallback_leakage_fix3\apply_phase154_r2_fix3.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fix3 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  tests/test_phase153_r3_11_reference_body_ownership_repair.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fix3 focused tests failed."
}

Write-Host ""
Write-Host "Representative Narrative check:"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=4,k=7); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); print(render_toda_group_proof_narrative_markdown(p))"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fix3 representative Narrative check failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fix3 focused verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
