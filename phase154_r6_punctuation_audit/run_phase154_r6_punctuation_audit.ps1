$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R6 - Punctuation Audit"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host ""

Write-Host "Current R5/R6 baseline focused contract:"
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
  throw "Phase 154-R6 punctuation audit baseline failed."
}

Write-Host ""
Write-Host "Running five-group punctuation audit..."
python ".\phase154_r6_punctuation_audit\audit_phase154_r6_punctuation.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6 punctuation audit failed."
}

Write-Host ""
Write-Host "Audit output:"
Write-Host "  .\phase154_r6_punctuation_audit\audit_output\phase154_r6_punctuation_audit.md"
Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R6 punctuation audit completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
