$ErrorActionPreference = "Stop"

$ProjectRoot = (Get-Location).Path
$PatchRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$ApplyScript = Join-Path $PatchRoot "apply_phase144_6_final_regression_repair_r10.py"
$TemporaryPackageMarker = Join-Path $ProjectRoot "tests\__init__.py"
$CreatedTemporaryPackageMarker = $false

Write-Host "=============================================================="
Write-Host "Phase 144-6 Final Regression Repair R10"
Write-Host "Generic Narrative regression repair"
Write-Host "=============================================================="

python $ApplyScript
if ($LASTEXITCODE -ne 0) {
  throw "R10 apply failed."
}

if (-not (Test-Path $TemporaryPackageMarker)) {
  New-Item -Path $TemporaryPackageMarker -ItemType File -Force | Out-Null
  $CreatedTemporaryPackageMarker = $true
  Write-Host "Temporary package marker created: tests/__init__.py"
}

$env:PYTHONPATH = "$ProjectRoot;$ProjectRoot\tests"

try {
  Write-Host ""
  Write-Host "Running focused regression set..."
  pytest -q `
    "tests/test_phase143_17_argument_discourse.py::test_phase143_17_pi16_9_discourse_roles" `
    "tests/test_phase143_46_multi_argument_narrative_assembler.py::test_phase143_46_pi16_9_assembles_definition_then_group_structure" `
    "tests/test_phase143_46_multi_argument_narrative_assembler.py::test_phase143_46_empty_arguments_render_empty_string" `
    "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py::test_phase143_47_pi16_9_suppresses_shared_definition_evidence" `
    "tests/test_phase143_51a_r_provenance_semantic_catalog.py::test_phase143_51a_r_pi15_8_suppresses_provenance_only_fallbacks" `
    "tests/test_phase143_51a_r_provenance_semantic_catalog.py::test_phase143_51a_r_pi16_9_suppresses_provenance_only_fallbacks" `
    "tests/test_phase143_51b_aggregate_statement_prose.py::test_phase143_51b_pi15_8_renders_short_exact_sequence" `
    "tests/test_phase143_51b_aggregate_statement_prose.py::test_phase143_51b_pi16_9_renders_order_and_e4_injective" `
    "tests/test_phase143_53a_r_aggregate_derivation.py::test_phase143_53a_r_pi16_9_aggregate_definition_stays_support"

  if ($LASTEXITCODE -ne 0) {
    throw "R10 focused regression set failed."
  }

  Write-Host ""
  Write-Host "Running directly related Phase 143 regression files..."
  pytest -q `
    "tests/test_phase143_17_argument_discourse.py" `
    "tests/test_phase143_46_multi_argument_narrative_assembler.py" `
    "tests/test_phase143_47_multi_argument_shared_contribution_dedup.py" `
    "tests/test_phase143_51a_r_provenance_semantic_catalog.py" `
    "tests/test_phase143_51b_aggregate_statement_prose.py" `
    "tests/test_phase143_53a_r_aggregate_derivation.py"

  if ($LASTEXITCODE -ne 0) {
    throw "R10 related Phase 143 regression files failed."
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 144-6 Final Regression Repair R10 focused tests: PASS"
  Write-Host "Full suite intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($CreatedTemporaryPackageMarker) {
    Remove-Item $TemporaryPackageMarker -Force -ErrorAction SilentlyContinue
    Write-Host "Temporary package marker removed: tests/__init__.py"
  }
}
