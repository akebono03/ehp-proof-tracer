$ErrorActionPreference="Stop"

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Final Repository Regression R1"
Write-Host "Canonical collection scope repair: tests/"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Documentation changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH=(Get-Location).Path
$env:PYTHONIOENCODING="utf-8"

if(-not (Test-Path ".\tests")){
  throw "Canonical tests/ directory was not found."
}

Write-Host ""
Write-Host "Running canonical repository regression suite exactly once..."
Write-Host "Command: pytest -q tests"
pytest -q tests
$exitCode=$LASTEXITCODE

Write-Host ""
Write-Host "=============================================================="
if($exitCode -eq 0){
  Write-Host "Phase 148 RC2-5 canonical repository regression: PASS"
  Write-Host "Do not run the full suite again."
  Write-Host "Send the complete pytest summary back for documentation closure."
} else {
  Write-Host "Phase 148 RC2-5 canonical repository regression: FAIL"
  Write-Host "Do not update documentation."
  Write-Host "Send the failure output back for classification."
}
Write-Host "=============================================================="

Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING

exit $exitCode
