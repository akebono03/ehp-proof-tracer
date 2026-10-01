$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R4 - Semantic Duplication / Transition Refinement"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Scope:"
Write-Host "  repeated generic FINAL_RESULT_DERIVATION prose only"
Write-Host "  reference linkage remains for R5"
Write-Host "  punctuation remains for R6"
Write-Host ""

Write-Host "Applying minimal production change..."
python ".\phase154_r4_semantic_duplication_transition_refinement\apply_phase154_r4.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R4 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r4_semantic_duplication_transition_refinement.py `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase150_rc4_7b_production_repair.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R4 focused tests failed."
}

Write-Host ""
Write-Host "Focused representative re-audit:"
python ".\phase154_r4_semantic_duplication_transition_refinement\audit_phase154_r4.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R4 focused re-audit failed."
}

Write-Host ""
Write-Host "Audit output:"
Write-Host "  .\phase154_r4_semantic_duplication_transition_refinement\audit_output\phase154_r4_summary.md"
Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R4 focused verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
