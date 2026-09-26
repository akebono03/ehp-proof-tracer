$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ag_impl_r2\repair_phase143_75ag_r2.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  pytest -q `
    ".\tests\test_phase72_lemma510_statement.py" `
    ".\tests\test_phase72_lemma510_modulo_integration.py" `
    ".\phase143_75ag_impl_r2\test_phase143_75ag_bracket_modulo_rendering.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Phase 143-75AG R2 focused implementation checks passed."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
