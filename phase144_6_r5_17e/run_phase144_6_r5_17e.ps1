$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_17e.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_17e.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_17e_proof_chain_architecture_decision.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_17e_proof_chain_architecture_decision.py") `
  -Force

Write-Host "Phase 144-6-R5-17E audit files applied."
Write-Host "Added/replaced only:"
Write-Host "  audit_phase144_6_r5_17e.py"
Write-Host "  tests/test_phase144_6_r5_17e_proof_chain_architecture_decision.py"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path
  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-17E targeted tests"
  Write-Host ("=" * 78)
  pytest -q ".\tests\test_phase144_6_r5_17e_proof_chain_architecture_decision.py"
  if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-17E audit"
  Write-Host ("=" * 78)
  python ".\audit_phase144_6_r5_17e.py"
  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
