$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75al\audit_phase143_75al.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected current baseline:"
  Write-Host "  fallback occurrences: 79"
  Write-Host "  target: 10 occurrences / 10 groups"
  Write-Host ""
  Write-Host "No pytest was run."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
