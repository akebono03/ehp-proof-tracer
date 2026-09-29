$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75aj_completion\audit_phase143_75aj_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AJ completion values:"
  Write-Host "  fallback occurrences: 89"
  Write-Host "  statement types: 19"
  Write-Host "  distinct fallback rule names: 20"
  Write-Host "  Toda36Lemma54SpecializationStatement: absent"
  Write-Host "  Toda Theorem 3.6 Lemma 5.4 specialization: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run by this completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
