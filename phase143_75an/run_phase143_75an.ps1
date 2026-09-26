$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75an\audit_phase143_75an.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected current baseline:"
  Write-Host "  fallback occurrences: 60"
  Write-Host "  target statement occurrences: 7"
  Write-Host "  target rule split: 5 + 2"
  Write-Host ""
  Write-Host "No pytest was run."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
