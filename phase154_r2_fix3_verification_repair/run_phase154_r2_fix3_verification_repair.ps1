$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fix3 - Verification Repair"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Repair: remove superseded Phase 153-R3.11 tests from the focused baseline"
Write-Host ""

Write-Host "Focused current-contract tests:"
python -m pytest `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase153_r7_proof_body_relevance.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  tests/test_phase153_closure_repair_r13.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fix3 current-contract verification failed."
}

Write-Host ""
Write-Host "Representative Narrative check:"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; r=build_standard_toda_report(n=4,k=7); g=r.candidates[0].source_candidate.group_result; p=build_toda_group_proof_presentation(build_toda_group_result_proof_replay(g,max_depth=2)); s=render_toda_group_proof_narrative_markdown(p); print(s); assert 'まず、[R2]を用いる。' in s; assert 'まず、[R2]\n' not in s; assert 'Toda Proposition 5.15を用いる。' not in s; assert r'\text{ is injective}' not in s; assert r'\text{ is exact}' not in s; assert 'である.を用いる。' not in s"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fix3 representative Narrative check failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fix3 current-contract verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
