$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R4 Fix1 - pi6_3 Residual Duplicate Audit"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Target: exact_duplicate_line_count=2 remaining in pi6_3"
Write-Host ""

Write-Host "R4 focused baseline:"
python -m pytest `
  tests/test_phase154_r4_semantic_duplication_transition_refinement.py `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase150_rc4_7b_production_repair.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R4 Fix1 baseline verification failed."
}

Write-Host ""
Write-Host "Running pi6_3 residual duplicate audit..."
python ".\phase154_r4_fix1_pi6_3_residual_duplicate_audit\audit_phase154_r4_fix1.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R4 Fix1 audit failed."
}

Write-Host ""
Write-Host "Audit output:"
Write-Host "  .\phase154_r4_fix1_pi6_3_residual_duplicate_audit\audit_output\phase154_r4_fix1_pi6_3_residual_duplicate_audit.md"
Write-Host "  .\phase154_r4_fix1_pi6_3_residual_duplicate_audit\audit_output\pi6_3_narrative.txt"
Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R4 Fix1 audit completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
