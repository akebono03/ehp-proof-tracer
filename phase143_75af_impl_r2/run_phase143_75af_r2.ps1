$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75af_impl_r2\repair_phase143_75af_r2.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  pytest -q `
    ".\tests\test_phase48_toda_prop44_first_summand_restriction.py" `
    ".\tests\test_phase48_toda_prop44_e_injective_applicability.py" `
    ".\phase143_75af_impl\test_phase143_75af_first_summand_rendering.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Phase 143-75AF R2 focused implementation checks passed."
  Write-Host "Production code was not changed by R2."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
