$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R5 Fix1 Repair2 - Legacy Route Linkage"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Repair:"
Write-Host "  invoke graph-backed Reference linkage after marker generation"
Write-Host "  and before body-usage Reference filtering in the legacy public route"
Write-Host ""

Write-Host "Applying Repair2..."
python ".\phase154_r5_fix1_repair2_legacy_route_linkage\apply_phase154_r5_fix1_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 Fix1 Repair2 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py `
  tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py `
  tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py `
  tests/test_phase154_r4_semantic_duplication_transition_refinement.py `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 Fix1 Repair2 focused tests failed."
}

Write-Host ""
Write-Host "Representative pi11_4 Narrative check:"
python ".\phase154_r5_fix1_repair2_legacy_route_linkage\check_phase154_r5_fix1_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 Fix1 Repair2 representative check failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R5 Fix1 Repair2 verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
