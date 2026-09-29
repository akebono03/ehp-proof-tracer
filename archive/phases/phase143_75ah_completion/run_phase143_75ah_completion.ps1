$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ah_completion\audit_phase143_75ah_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AH completion values:"
  Write-Host "  fallback occurrences: 116"
  Write-Host "  statement types: 21"
  Write-Host "  distinct fallback rule names: 22"
  Write-Host "  TodaLemma57TwoIota5ImageMembershipStatement: absent"
  Write-Host "  Toda Lemma 5.7 nu-prime hypothesis: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run by this completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
