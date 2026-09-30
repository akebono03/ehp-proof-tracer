$ErrorActionPreference="Stop"

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Final Regression Repair R2"
Write-Host "Restore Phase 144-6 generic production-route test contract"
Write-Host "Production changes: none"
Write-Host "Documentation changes: none"
Write-Host "Repository-wide pytest: NOT run"
Write-Host "=============================================================="

$env:PYTHONPATH=(Get-Location).Path
$env:PYTHONIOENCODING="utf-8"

Write-Host ""
Write-Host "A. Applying test-contract restoration..."
python ".\phase148_rc2_5_final_regression_repair_r2_restore_phase144_6_contract\apply_phase148_rc2_5_final_regression_repair_r2.py"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile ".\tests\test_phase144_6_pi6_generic_production_route.py"
if($LASTEXITCODE -ne 0){ exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. Running only the repaired Phase 144-6 contract tests..."
pytest -q ".\tests\test_phase144_6_pi6_generic_production_route.py"
$exitCode=$LASTEXITCODE

Write-Host ""
Write-Host "=============================================================="
if($exitCode -eq 0){
  Write-Host "Phase 148 RC2-5 Final Regression Repair R2 focused tests: PASS"
  Write-Host "Do NOT rerun repository-wide pytest."
  Write-Host "Return this output for Phase 148 documentation closure."
}else{
  Write-Host "Phase 148 RC2-5 Final Regression Repair R2 focused tests: FAIL"
  Write-Host "Do NOT update documentation."
}
Write-Host "=============================================================="

Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING
exit $exitCode
