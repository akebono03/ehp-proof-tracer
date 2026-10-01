$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154-R6-2 - ASCII Comma Normalization"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Policy:"
Write-Host "  comma: , + space"
Write-Host "  period: ."
Write-Host "  TeX / math punctuation: unchanged"
Write-Host ""

python ".\phase154_r6_2_ascii_comma_normalization\apply_phase154_r6_2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-2 apply failed."
}

Write-Host ""
Write-Host "Focused tests:"
python -m pytest `
  tests/test_phase154_r6_2_ascii_comma_normalization.py `
  tests/test_phase154_r6_1_repair3_ascii_period_policy.py `
  tests/test_phase154_r5_fix1_repair2_legacy_route_linkage.py `
  tests/test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py `
  tests/test_phase154_r5_fix1_graph_backed_reference_linkage.py `
  tests/test_phase154_r2_internal_prose_fallback_leakage.py `
  tests/test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py `
  tests/test_phase154_r2_fix2_semantic_sentence_composition.py `
  tests/test_phase154_r2_fix3_reference_marker_completion.py `
  tests/test_phase153_r8_reference_use_prose_normalization.py `
  tests/test_phase143_17_argument_discourse.py `
  tests/test_phase143_30_exactness_method_transition.py `
  tests/test_phase143_34_argument_header_method.py `
  tests/test_phase150_rc4_5b_3_reference_binding.py `
  tests/test_phase150_rc4_5c_2_exactness_to_map_property.py `
  tests/test_phase150_rc4_5e_2_short_exact_derivation_reason.py `
  -q

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-2 focused tests failed."
}

Write-Host ""
Write-Host "Five-group punctuation re-audit:"
python ".\phase154_r6_2_ascii_comma_normalization\audit_phase154_r6_2.py"

if ($LASTEXITCODE -ne 0) {
  throw "Phase 154-R6-2 punctuation re-audit failed."
}

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154-R6-2 verification completed"
Write-Host "=============================================================================="
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
