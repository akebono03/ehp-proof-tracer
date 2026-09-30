$ErrorActionPreference="Stop"

Write-Host "=============================================================="
Write-Host "Phase 148 RC2-5 Final Repository Regression"
Write-Host "Production changes: none"
Write-Host "Test changes: none"
Write-Host "Documentation changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH=(Get-Location).Path
$env:PYTHONIOENCODING="utf-8"

Write-Host ""
Write-Host "Running repository-wide pytest exactly once..."
pytest -q
$exitCode=$LASTEXITCODE

Write-Host ""
Write-Host "=============================================================="
if($exitCode -eq 0){
  Write-Host "Phase 148 RC2-5 repository-wide pytest: PASS"
  Write-Host "Do not run pytest again."
  Write-Host "Send the complete pytest summary back for documentation closure."
} else {
  Write-Host "Phase 148 RC2-5 repository-wide pytest: FAIL"
  Write-Host "Do not update documentation."
  Write-Host "Send the failure output back for classification."
}
Write-Host "=============================================================="

Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING

exit $exitCode
