$ErrorActionPreference="Stop"
$PackageRoot=Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot=(Get-Location).Path
$TestsDir=Join-Path $RepoRoot "tests"
$Marker=Join-Path $TestsDir "__init__.py"
$CreatedMarker=$false
$OldPythonPath=$env:PYTHONPATH
$OldEncoding=$env:PYTHONIOENCODING

Write-Host "=============================================================="
Write-Host "Phase 144 Final Regression Repair R2"
Write-Host "One production depth-boundary repair + stale expectation maintenance"
Write-Host "Whole-suite pytest: NOT run"
Write-Host "=============================================================="

try {
  $env:PYTHONPATH="$RepoRoot;$TestsDir"
  $env:PYTHONIOENCODING="utf-8"
  if (-not (Test-Path $Marker)) {
    New-Item -ItemType File -Path $Marker -Force | Out-Null
    $CreatedMarker=$true
  }

  Write-Host ""
  Write-Host "A. Applying minimal repair..."
  python (Join-Path $PackageRoot "apply_phase144_final_regression_repair_r2.py")
  if ($LASTEXITCODE -ne 0) { throw "R2 patch failed." }

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\main.py" `
    ".\tests\test_phase132_7_group_proof_cli_modes.py" `
    ".\tests\test_phase133_10_sigma_label_wording.py" `
    ".\tests\test_phase143_47_multi_argument_shared_contribution_dedup.py" `
    ".\tests\test_phase143_50_generic_statement_prose_renderer.py" `
    ".\tests\test_phase143_58a_negative_scalar_sum.py" `
    ".\tests\test_phase143_59b_group_structure_duplicate_suppression.py" `
    ".\tests\test_phase143_61b_direct_premise_narrative.py"
  if ($LASTEXITCODE -ne 0) { throw "Syntax preflight failed." }

  Write-Host ""
  Write-Host "C. Re-running the eight remaining failures only..."
  python -m pytest -q `
    "tests/test_phase132_7_group_proof_cli_modes.py::test_phase132_7_group_proof_depth_zero_is_shared_across_modes[narrative-# Group proof narrative]" `
    "tests/test_phase133_10_sigma_label_wording.py::test_phase133_10_sigma9_depth_two_uses_final_japanese_wording" `
    "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py::test_phase143_47_pi8_5_suppresses_shared_exactness_contributions" `
    "tests/test_phase143_50_generic_statement_prose_renderer.py::test_phase143_50_pi6_3_renders_map_properties_in_japanese" `
    "tests/test_phase143_50_generic_statement_prose_renderer.py::test_phase143_50_structured_prose_remains_after_aggregate_rendering" `
    "tests/test_phase143_58a_negative_scalar_sum.py::test_phase143_58a_pi6_3_narrative_normalizes_negative_scalar_sum" `
    "tests/test_phase143_59b_group_structure_duplicate_suppression.py::test_phase143_59b_pi6_3_narrative_remains_available" `
    "tests/test_phase143_61b_direct_premise_narrative.py::test_phase143_61b_pi8_5_direct_premise_is_not_left_at_argument_start"
  if ($LASTEXITCODE -ne 0) { throw "R2 focused rerun failed. Do NOT run the whole suite." }

  Write-Host ""
  Write-Host "D. Phase144-6 production-route controls..."
  python -m pytest -q `
    "tests/test_phase144_6_pi6_generic_production_route.py" `
    "tests/test_phase144_6_public_route_cutover.py"
  if ($LASTEXITCODE -ne 0) { throw "Production-route controls failed. Do NOT run the whole suite." }

  Write-Host ""
  Write-Host "E. Current changes..."
  git status --short
  git diff --stat -- main.py tests

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144 Final Regression Repair R2 focused tests: PASS"
  Write-Host "Whole-suite pytest was NOT run."
  Write-Host "=============================================================="
}
finally {
  if ($null -eq $OldPythonPath) { Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue } else { $env:PYTHONPATH=$OldPythonPath }
  if ($null -eq $OldEncoding) { Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue } else { $env:PYTHONIOENCODING=$OldEncoding }
  if ($CreatedMarker -and (Test-Path $Marker)) { Remove-Item $Marker -Force }
}
