$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  pytest -q `
    ".\tests\test_phase72_lemma510_statement.py" `
    ".\tests\test_phase72_lemma510_modulo_integration.py" `
    ".\phase143_75ag_r5_completion\test_phase143_75ag_bracket_modulo_rendering.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Focused tests passed."
  Write-Host ""

  python ".\phase143_75ag_r5_completion\audit_phase143_75ag_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AG completion values:"
  Write-Host "  fallback occurrences: 133"
  Write-Host "  statement types: 22"
  Write-Host "  distinct fallback rule names: 23"
  Write-Host "  TodaLemma510BracketModuloStatement: absent"
  Write-Host "  corrected ordinary modulo integration: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
