$ErrorActionPreference="Stop"
$PackageRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot=(Get-Location).Path
$TestsDir=Join-Path $RepoRoot "tests"
$Marker=Join-Path $TestsDir "__init__.py"
$CreatedMarker=$false
$OldPythonPath=$env:PYTHONPATH
$OldEncoding=$env:PYTHONIOENCODING

Write-Host "=============================================================="
Write-Host "Phase 144 Final Regression Repair R1"
Write-Host "Confirmed stale-test maintenance only"
Write-Host "Production changes: none"
Write-Host "Whole-suite pytest: NOT run"
Write-Host "=============================================================="

try {
  Write-Host ""
  Write-Host "A. Applying confirmed test maintenance..."
  Copy-Item `
    (Join-Path $PackageRoot "payload\tests\test_phase144_6_pi6_generic_production_route.py") `
    (Join-Path $RepoRoot "tests\test_phase144_6_pi6_generic_production_route.py") `
    -Force
  Copy-Item `
    (Join-Path $PackageRoot "payload\tests\test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py") `
    (Join-Path $RepoRoot "tests\test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py") `
    -Force
  Copy-Item `
    (Join-Path $PackageRoot "payload\tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py") `
    (Join-Path $RepoRoot "tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py") `
    -Force
  Copy-Item `
    (Join-Path $PackageRoot "payload\tests\test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py") `
    (Join-Path $RepoRoot "tests\test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py") `
    -Force

  if (-not (Test-Path $Marker)) {
    New-Item -ItemType File -Path $Marker -Force | Out-Null
    $CreatedMarker=$true
  }

  $env:PYTHONPATH="$RepoRoot;$TestsDir"
  $env:PYTHONIOENCODING="utf-8"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\tests\test_phase144_6_pi6_generic_production_route.py" `
    ".\tests\test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py" `
    ".\tests\test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py" `
    ".\tests\test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py"
  if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

  Write-Host ""
  Write-Host "C. Re-running only the 14 failures observed in the interrupted full suite..."
  python -m pytest -q `
    "tests/test_phase132_7_group_proof_cli_modes.py::test_phase132_7_group_proof_depth_zero_is_shared_across_modes[narrative-# Group proof narrative]" `
    "tests/test_phase133_10_sigma_label_wording.py::test_phase133_10_sigma9_depth_two_uses_final_japanese_wording" `
    "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py::test_phase143_47_pi8_5_suppresses_shared_exactness_contributions" `
    "tests/test_phase143_50_generic_statement_prose_renderer.py::test_phase143_50_pi6_3_renders_map_properties_in_japanese" `
    "tests/test_phase143_50_generic_statement_prose_renderer.py::test_phase143_50_structured_prose_remains_after_aggregate_rendering" `
    "tests/test_phase143_58a_negative_scalar_sum.py::test_phase143_58a_pi6_3_narrative_normalizes_negative_scalar_sum" `
    "tests/test_phase143_59b_group_structure_duplicate_suppression.py::test_phase143_59b_pi6_3_narrative_remains_available" `
    "tests/test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi8_5_direct_premise_is_not_left_at_argument_start" `
    "tests/test_phase144_6_pi6_generic_production_route.py::test_phase144_6_public_pi6_3_narrative_equals_generic_argument_renderer" `
    "tests/test_phase144_6_pi6_generic_production_route.py::test_phase144_6_cli_pi6_3_narrative_uses_generic_route" `
    "tests/test_phase144_6_pi6_generic_production_route.py::test_phase144_6_pi6_production_branch_contains_no_legacy_renderer_call" `
    "tests/test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py::test_phase144_6_r5_37_inventory_is_phase36_missing_population" `
    "tests/test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py::test_phase144_6_r5_38_visibility_population_matches_phase37" `
    "tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py::test_phase144_6_r5_39_inventory_matches_phase38_contribution_count"
  $FocusedExit=$LASTEXITCODE

  Write-Host ""
  Write-Host "D. Current git diff summary..."
  git status --short
  git diff --stat -- `
    "tests/test_phase144_6_pi6_generic_production_route.py" `
    "tests/test_phase144_6_r5_37_genuinely_missing_semantic_equivalence_and_rendering_audit.py" `
    "tests/test_phase144_6_r5_38_visibility_gap_explanatory_contribution_dedup_ownership_audit.py" `
    "tests/test_phase144_6_r5_39_explanatory_contribution_narrative_necessity_audit.py"

  if ($FocusedExit -ne 0) {
    throw "Focused 14-failure rerun still has failures. Do NOT run the whole suite."
  }

  Write-Host ""
  Write-Host "Phase 144 Final Regression Repair R1 focused rerun: PASS"
  Write-Host "Do NOT run the whole suite yet."
}
finally {
  if ($null -eq $OldPythonPath) {
    Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONPATH=$OldPythonPath
  }
  if ($null -eq $OldEncoding) {
    Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
  } else {
    $env:PYTHONIOENCODING=$OldEncoding
  }
  if ($CreatedMarker -and (Test-Path $Marker)) {
    Remove-Item $Marker -Force
  }
}
