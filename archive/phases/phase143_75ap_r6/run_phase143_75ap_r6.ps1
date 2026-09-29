$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ap_r6\apply_phase143_75ap_r6.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  pytest -q `
    ".\tests\test_phase72r5_ordinary_ehp_211_exactness.py" `
    ".\tests\test_phase72r7_primary_composition_indeterminacy.py" `
    ".\tests\test_phase72r9_corrected_provenance_retirement.py" `
    ".\tests\test_phase75_515_sigma8_prop44_specialization.py" `
    ".\tests\test_phase75_515_sigma8_transported_decomposition.py" `
    ".\tests\test_phase100_prop515_upper_bootstrap.py" `
    ".\tests\test_phase134_24_pi15_8_narrative.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 143-75AP R6 focused tests passed."
  Write-Host "=============================================================="
  Write-Host "Next: remaining-fallback completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
