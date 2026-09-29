$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 146 Final Regression Expectation Repair R2"
Write-Host "Production changes: none"
Write-Host "Remaining group-purpose expectation + CRLF restoration"
Write-Host "=============================================================="

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir
Set-Location $RepoRoot

Write-Host "`nA. Applying R2..."
python "$PackageDir\apply_phase146_final_regression_expectation_repair_r2.py"

Write-Host "`nB. Syntax preflight..."
python -m py_compile tests\test_phase143_34_argument_header_method.py tests\test_phase143_44_single_argument_narrative_renderer.py tests\test_phase143_46_multi_argument_narrative_assembler.py tests\test_phase144_5_generic_definition_order_equations.py tests\test_phase144_6_pi6_generic_production_route.py

Write-Host "`nC. Re-running affected test files..."
python -m pytest -q tests\test_phase143_34_argument_header_method.py tests\test_phase143_44_single_argument_narrative_renderer.py tests\test_phase143_46_multi_argument_narrative_assembler.py tests\test_phase144_5_generic_definition_order_equations.py tests\test_phase144_6_pi6_generic_production_route.py

Write-Host "`nD. Verifying diff size..."
git diff --numstat -- tests/test_phase143_34_argument_header_method.py tests/test_phase143_44_single_argument_narrative_renderer.py tests/test_phase143_46_multi_argument_narrative_assembler.py tests/test_phase144_5_generic_definition_order_equations.py tests/test_phase144_6_pi6_generic_production_route.py
git diff --stat -- tests/test_phase143_34_argument_header_method.py tests/test_phase143_44_single_argument_narrative_renderer.py tests/test_phase143_46_multi_argument_narrative_assembler.py tests/test_phase144_5_generic_definition_order_equations.py tests/test_phase144_6_pi6_generic_production_route.py

Write-Host "`n=============================================================="
Write-Host "R2 focused repair complete."
Write-Host "If PASS and diff is small, final suite:"
Write-Host "  python -m pytest tests -q --durations=50"
Write-Host "=============================================================="
