$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  pytest -q `
    ".\tests\test_phase67_lemma57_hypothesis_statement.py" `
    ".\tests\test_phase67_lemma57_nu_prime_specialization.py" `
    ".\phase143_75ah_r2\test_phase143_75ah_two_iota5_rendering.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Phase 143-75AH R2 focused checks passed."
  Write-Host "Production code was not changed by R2."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
