$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fix3 - Verification Repair Fixed2"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Repair: add repository root to sys.path in the representative check"
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
python ".\phase154_r2_fix3_verification_repair_fixed2\check_phase154_r2_fix3_representative_narrative.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R2 Fix3 representative Narrative check failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R2 Fix3 current-contract verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
