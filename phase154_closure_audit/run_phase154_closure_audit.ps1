$ErrorActionPreference = "Stop"

$PackageDir = $PSScriptRoot
$RepoRoot = Split-Path -Parent $PackageDir

function Invoke-NativeChecked {
  param(
    [Parameter(Mandatory = $true)]
    [scriptblock]$Command,
    [Parameter(Mandatory = $true)]
    [string]$Label
  )

  & $Command

  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE."
  }
}

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase 154 - Closure Audit"
Write-Host "=============================================================================="
Write-Host "Repository:"
Write-Host "  $RepoRoot"
Write-Host ""
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full test suite: NOT RUN"
Write-Host ""

Write-Host "[1/4] Compile audit"
Invoke-NativeChecked `
  -Label "compile audit" `
  -Command {
    python -m py_compile `
      "$PackageDir\audit_phase154_closure.py"
  }

Write-Host ""
Write-Host "[2/4] Phase 154 focused regression"
Invoke-NativeChecked `
  -Label "Phase 154 focused regression" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase154_r2_internal_prose_fallback_leakage.py" `
      ".\tests\test_phase154_r2_fixed1_nu4_decomposition_semantic_prose.py" `
      ".\tests\test_phase154_r2_fix2_semantic_sentence_composition.py" `
      ".\tests\test_phase154_r2_fix3_reference_marker_completion.py" `
      ".\tests\test_phase154_r4_semantic_duplication_transition_refinement.py" `
      ".\tests\test_phase154_r5_fix1_graph_backed_reference_linkage.py" `
      ".\tests\test_phase154_r5_fix1_repair1_reference_entry_frontier_linkage.py" `
      ".\tests\test_phase154_r5_fix1_repair2_legacy_route_linkage.py" `
      ".\tests\test_phase154_r6_1_repair3_ascii_period_policy.py" `
      ".\tests\test_phase154_r6_2_ascii_comma_normalization.py" `
      ".\tests\test_phase154_r6_2_repair1_missing_shared_sources.py" `
      ".\tests\test_phase154_r6_2_repair2_equation_numbering.py"
  }

Write-Host ""
Write-Host "[3/4] Ordering / reason regression boundary"
Invoke-NativeChecked `
  -Label "ordering / reason regression boundary" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
      ".\tests\test_phase149_rc3_4_cross_group_ordering.py" `
      ".\tests\test_phase150_rc4_4_reasons.py" `
      ".\tests\test_phase150_rc4_5_visible_reasons.py" `
      ".\tests\test_phase150_rc4_5b_3_reference_binding.py" `
      ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
      ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
      ".\tests\test_phase150_rc4_5f_2_final_group_structure_reason.py" `
      ".\tests\test_phase150_rc4_7d_generic_reason_vocabulary.py" `
      ".\tests\test_phase150_rc4_closure_reason_visibility.py"
  }

Write-Host ""
Write-Host "[4/4] 112-group Phase 154 closure audit"
Invoke-NativeChecked `
  -Label "112-group Phase 154 closure audit" `
  -Command {
    python "$PackageDir\audit_phase154_closure.py"
  }

Write-Host ""
Write-Host "=============================================================================="
Write-Host "Phase 154 Closure Audit completed successfully."
Write-Host "=============================================================================="
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "Full test suite: NOT RUN (reserved for phase end)"
Write-Host "If this passes, next step is Phase 154 documentation closure,"
Write-Host "then Phase 154 final full regression."
