$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ak_completion\audit_phase143_75ak_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AK completion values:"
  Write-Host "  fallback occurrences: 79"
  Write-Host "  statement types: 18"
  Write-Host "  distinct fallback rule names: 19"
  Write-Host "  TodaLemma514SigmaDoublePrimeStatement: absent"
  Write-Host "  Toda Lemma 5.14 sigma double-prime branch: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run by this completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
