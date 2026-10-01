$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R3 - Cross-group Prose Re-audit"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Narrative depth: 2"
Write-Host ""

Write-Host "R2 current-contract baseline:"
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
  throw "Phase 154-R3 baseline verification failed."
}

Write-Host ""
Write-Host "Running cross-group prose re-audit..."
python ".\phase154_r3_cross_group_prose_reaudit\audit_phase154_r3.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R3 audit failed."
}

Write-Host ""
Write-Host "Audit output:"
Write-Host "  .\phase154_r3_cross_group_prose_reaudit\audit_output\phase154_r3_summary.md"
Write-Host "  .\phase154_r3_cross_group_prose_reaudit\audit_output\pi6_3.md"
Write-Host "  .\phase154_r3_cross_group_prose_reaudit\audit_output\pi10_4.md"
Write-Host "  .\phase154_r3_cross_group_prose_reaudit\audit_output\pi11_4.md"
Write-Host "  .\phase154_r3_cross_group_prose_reaudit\audit_output\pi12_5.md"
Write-Host "  .\phase154_r3_cross_group_prose_reaudit\audit_output\pi16_9.md"
Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R3 audit completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
