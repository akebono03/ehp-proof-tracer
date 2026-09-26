$ErrorActionPreference = "Stop"

$env:PYTHONPATH = (Get-Location).Path

try {
  python ".\phase143_75ap_r11_r4\apply_phase143_75ap_r11_r4.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  pytest -q `
    ".\tests\test_phase143_51a_r_provenance_semantic_catalog.py" `
    ".\tests\test_phase143_51b_aggregate_statement_prose.py" `
    ".\tests\test_phase134_24_pi15_8_narrative.py"

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 143-75AP R11-R4 focused tests passed."
  Write-Host "=============================================================="
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
