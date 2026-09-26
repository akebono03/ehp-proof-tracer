$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ad\audit_phase143_75ad.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected baseline:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  current fallback occurrences: 216"
  Write-Host "  target: 20 occurrences / 18 groups"
  Write-Host "  target rule: Toda Lemma 5.4 double suspension up to sign"
  Write-Host "  current semantic rendering: None"
  Write-Host ""
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
