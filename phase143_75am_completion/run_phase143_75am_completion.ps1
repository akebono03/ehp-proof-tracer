$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75am_completion\audit_phase143_75am_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AM completion values:"
  Write-Host "  fallback occurrences: 60"
  Write-Host "  statement types: 16"
  Write-Host "  distinct fallback rule names: 17"
  Write-Host "  Toda514SecondShortExactStatement: absent"
  Write-Host "  Toda (5.14) second short exact sequence: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run by this completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
