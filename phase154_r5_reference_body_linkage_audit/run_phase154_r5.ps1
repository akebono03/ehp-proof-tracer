$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R5 - Reference <-> Proof Body Linkage Audit"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Target: pi11_4 [R1] / [R2] linkage"
Write-Host ""

Write-Host "Current focused baseline:"
python -m pytest `
  tests/test_phase154_r4_semantic_duplication_transition_refinement.py `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 baseline verification failed."
}

Write-Host ""
Write-Host "Running Reference linkage graph audit..."
python ".\phase154_r5_reference_body_linkage_audit\audit_phase154_r5.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R5 linkage audit failed."
}

Write-Host ""
Write-Host "Audit output:"
Write-Host "  .\phase154_r5_reference_body_linkage_audit\audit_output\phase154_r5_reference_body_linkage_audit.md"
Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R5 initial audit completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
