$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R6-1 Repair2 - Idempotent Resume"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "This repair safely resumes after the partially applied Repair1."
Write-Host "Already-current punctuation is accepted and left unchanged."
Write-Host ""

python ".\phase154_r6_1_repair2_idempotent_resume\apply_phase154_r6_1_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-1 Repair2 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r6_1_shared_punctuation_normalization.py `
  tests/test_phase154_r6_1_repair2_idempotent_resume.py `
  tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py `
  tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py `
  tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-1 Repair2 focused tests failed."
}

Write-Host ""
Write-Host "Five-group punctuation re-audit:"
python ".\phase154_r6_1_repair2_idempotent_resume\audit_phase154_r6_1_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-1 Repair2 punctuation re-audit failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R6-1 Repair2 verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
