$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75an_impl\repair_phase143_75an.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  pytest -q `
    ".\tests\test_phase60_toda54_indeterminacy.py" `
    ".\phase143_75an_impl\test_phase143_75an_indeterminacy_rendering.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Phase 143-75AN focused checks passed."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
