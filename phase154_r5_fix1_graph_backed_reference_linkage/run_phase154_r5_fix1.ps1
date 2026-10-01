$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R5 Fix1 - Graph-backed Reference Linkage"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Scope:"
Write-Host "  selected Reference step -> unique visible non-root consumer"
Write-Host "  ambiguous/root-only linkage keeps neutral reference-use prose"
Write-Host ""

Write-Host "Applying minimal production change..."
python ".\phase154_r5_fix1_graph_backed_reference_linkage\apply_phase154_r5_fix1.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 Fix1 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py `
  tests/test_phase154_r4_semantic_duplication_transition_refinement.py `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 Fix1 focused tests failed."
}

Write-Host ""
Write-Host "Representative pi11_4 Narrative check:"
python ".\phase154_r5_fix1_graph_backed_reference_linkage\check_phase154_r5_fix1_pi11_4.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 Fix1 representative check failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R5 Fix1 focused verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
