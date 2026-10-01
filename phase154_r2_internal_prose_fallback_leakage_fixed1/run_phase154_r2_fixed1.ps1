$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fixed1 - Nu4 Decomposition Semantic Prose"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Assumption: initial Phase 154-R2 patch is already applied."
Write-Host ""

Write-Host "Applying Fixed1..."
python ".\phase154_r2_internal_prose_fallback_leakage_fixed1\apply_phase154_r2_fixed1.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fixed1 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase143_50_generic_statement_prose_renderer.py `
  tests/test_phase143_51a_r_provenance_semantic_catalog.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fixed1 focused tests failed."
}

Write-Host ""
Write-Host "Representative Narrative check:"
python -c "from toda_calculation_facade import build_standard_toda_report; from toda_group_result_proof_replay import build_toda_group_result_proof_replay; from toda_group_proof_presentation import build_toda_group_proof_presentation; from toda_group_proof_narrative_renderer import render_toda_group_proof_narrative_markdown; [(print('---', n, k), print(render_toda_group_proof_narrative_markdown(build_toda_group_proof_presentation(build_toda_group_result_proof_replay(build_standard_toda_report(n=n,k=k).candidates[0].source_candidate.group_result,max_depth=2))))) for n,k in ((4,6),(4,7))]"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fixed1 representative Narrative check failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fixed1 focused verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
