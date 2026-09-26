$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ap_r9\apply_phase143_75ap_r9.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  pytest -q `
    ".\tests\test_phase143_51a_r_provenance_semantic_catalog.py" `
    ".\tests\test_phase143_51b_aggregate_statement_prose.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 143-75AP R9 focused regression passed."
  Write-Host "=============================================================="
  Write-Host "Next: rerun the canonical full Phase 143 regression."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
