$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R6-2 Repair2 - Equation Numbering and R6-1 Test Repair"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Repairs:"
Write-Host "  argument-body derivation connector"
Write-Host "  equation-numbering derivation connector"
Write-Host "  R6-1 audit-test predicate damaged by prior global test replacement"
Write-Host ""

python ".\phase154_r6_2_repair2_equation_numbering_and_r6_1_test\apply_phase154_r6_2_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-2 Repair2 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r6_2_ascii_comma_normalization.py `
  tests/test_phase154_r6_2_repair1_missing_shared_sources.py `
  tests/test_phase154_r6_2_repair2_equation_numbering.py `
  tests/test_phase154_r6_1_repair3_ascii_period_policy.py `
  tests/test_phase143_57c_step_derivation_connector.py `
  tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py `
  tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py `
  tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  tests/test_phase143_30_exactness_method_transition.py `
  tests/test_phase143_34_argument_header_method.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-2 Repair2 focused tests failed."
}

Write-Host ""
Write-Host "Five-group punctuation re-audit:"
python ".\phase154_r6_2_repair2_equation_numbering_and_r6_1_test\audit_phase154_r6_2_repair2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-2 Repair2 punctuation re-audit failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R6-2 Repair2 verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
