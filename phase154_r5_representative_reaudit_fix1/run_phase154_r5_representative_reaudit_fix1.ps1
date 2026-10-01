$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R5 - Representative Re-audit Fix1"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Fix: exclude Reference-section headings from proof-body marker defects"
Write-Host ""

Write-Host "Current R5 focused contract:"
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
  throw "Phase 154-R5 re-audit Fix1 baseline failed."
}

Write-Host ""
Write-Host "Running corrected five-group Reference linkage re-audit..."
python ".\phase154_r5_representative_reaudit_fix1\audit_phase154_r5_representatives_fix1.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 re-audit Fix1 failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R5 representative re-audit Fix1 completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
