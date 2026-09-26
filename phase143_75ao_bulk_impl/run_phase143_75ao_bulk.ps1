$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ao_bulk_impl\repair_phase143_75ao_bulk.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  pytest -q `
    ".\tests\test_phase72r4_serre_finiteness.py" `
    ".\tests\test_phase72r5_ordinary_ehp_211_exactness.py" `
    ".\tests\test_phase72r6_ordinary_primary_bridge.py" `
    ".\tests\test_phase72_lemma510_core_inference.py" `
    ".\tests\test_phase72r8_corrected_lemma510_integration.py" `
    ".\phase143_75ao_bulk_impl\test_phase143_75ao_bulk_rendering.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Phase 143-75AO bulk focused checks passed."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
