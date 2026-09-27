$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_17a.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_17a.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_17a_proof_chain_selection_audit.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_17a_proof_chain_selection_audit.py") `
  -Force

Write-Host "Phase 144-6-R5-17A-R1 diagnostic repair applied."
Write-Host "Replaced only:"
Write-Host "  audit_phase144_6_r5_17a.py"
Write-Host "  tests/test_phase144_6_r5_17a_proof_chain_selection_audit.py"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-17A-R1 targeted tests"
  Write-Host ("=" * 78)
  pytest -q ".\tests\test_phase144_6_r5_17a_proof_chain_selection_audit.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-17A-R1 diagnostic audit"
  Write-Host ("=" * 78)
  python ".\audit_phase144_6_r5_17a.py"
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
