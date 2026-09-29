$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  python ".\phase143_75ae\audit_phase143_75ae.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ""
  Write-Host "Expected baseline:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  current fallback occurrences: 196"
  Write-Host "  target: 25 occurrences / 13 groups"
  Write-Host "  13 x Toda Proposition 5.11 E pi_8^2 zero"
  Write-Host "  12 x Toda Proposition 5.11 E pi_7^2 zero"
  Write-Host "  current semantic rendering: None"
  Write-Host ""
  Write-Host "Do not run the full pytest suite yet."
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
