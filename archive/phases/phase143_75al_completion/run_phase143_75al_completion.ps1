$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75al_completion\audit_phase143_75al_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AL completion values:"
  Write-Host "  fallback occurrences: 69"
  Write-Host "  statement types: 17"
  Write-Host "  distinct fallback rule names: 18"
  Write-Host "  Toda514FirstShortExactStatement: absent"
  Write-Host "  Toda (5.14) first short exact sequence: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run by this completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
