$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ao_bulk_audit\audit_phase143_75ao_bulk.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected current baseline:"
  Write-Host "  fallback occurrences: 53"
  Write-Host "  statement types: 15"
  Write-Host "  distinct fallback rule names: 15"
  Write-Host "  render errors: 0"
  Write-Host ""
  Write-Host "No pytest was run."
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
