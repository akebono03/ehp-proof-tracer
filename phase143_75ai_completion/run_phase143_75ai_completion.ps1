$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ai_completion\audit_phase143_75ai_completion.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected Phase 143-75AI completion values:"
  Write-Host "  fallback occurrences: 101"
  Write-Host "  statement types: 20"
  Write-Host "  distinct fallback rule names: 21"
  Write-Host "  TodaProp59DeltaKernelStatement: absent"
  Write-Host "  Toda Proposition 5.9 Delta nu_5 kernel: absent"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run by this completion audit."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
