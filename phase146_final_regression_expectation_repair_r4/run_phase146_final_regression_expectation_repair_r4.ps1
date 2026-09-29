$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 146 Final Regression Expectation Repair R4"
Write-Host "Newline-aware clean minimal diff repair"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

Write-Host "`nA. Restore from HEAD + newline-aware minimal edits..."
python "$PackageDir\apply_phase146_final_regression_expectation_repair_r4.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nB. Syntax preflight..."
python -m py_compile tests\test_phase143_34_argument_header_method.py tests\test_phase143_44_single_argument_narrative_renderer.py tests\test_phase143_46_multi_argument_narrative_assembler.py tests\test_phase144_5_generic_definition_order_equations.py tests\test_phase144_6_pi6_generic_production_route.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nC. Focused tests..."
python -m pytest -q tests\test_phase143_34_argument_header_method.py tests\test_phase143_44_single_argument_narrative_renderer.py tests\test_phase143_46_multi_argument_narrative_assembler.py tests\test_phase144_5_generic_definition_order_equations.py tests\test_phase144_6_pi6_generic_production_route.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nD. Minimal-diff verification..."
git diff --numstat -- tests/test_phase143_34_argument_header_method.py tests/test_phase143_44_single_argument_narrative_renderer.py tests/test_phase143_46_multi_argument_narrative_assembler.py tests/test_phase144_5_generic_definition_order_equations.py tests/test_phase144_6_pi6_generic_production_route.py

git diff --check -- tests/test_phase143_34_argument_header_method.py tests/test_phase143_44_single_argument_narrative_renderer.py tests/test_phase143_46_multi_argument_narrative_assembler.py tests/test_phase144_5_generic_definition_order_equations.py tests/test_phase144_6_pi6_generic_production_route.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "`nE. Exact diff..."
git diff -- tests/test_phase143_34_argument_header_method.py tests/test_phase143_44_single_argument_narrative_renderer.py tests/test_phase143_46_multi_argument_narrative_assembler.py tests/test_phase144_5_generic_definition_order_equations.py tests/test_phase144_6_pi6_generic_production_route.py

Write-Host "`n=============================================================="
Write-Host "R4 complete."
Write-Host "Expected: 31 passed; all five files have only small diffs."
Write-Host "Then run: python -m pytest tests -q --durations=50"
Write-Host "=============================================================="
