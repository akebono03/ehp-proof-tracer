$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ak_impl\repair_phase143_75ak.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  pytest -q `
    ".\tests\test_phase75_lemma514_sigma_double_prime.py" `
    ".\phase143_75ak_impl\test_phase143_75ak_sigma_double_prime_rendering.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Phase 143-75AK focused checks passed."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
