$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75an_completion\audit_phase143_75an_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AN completion values:"
  Write-Host "  fallback occurrences: 53"
  Write-Host "  statement types: 15"
  Write-Host "  distinct fallback rule names: 15"
  Write-Host "  Toda54IndeterminacyGeneratorStatement: absent"
  Write-Host "  double nu-prime generator bridge: absent"
  Write-Host "  eta triple composition: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run by this completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
