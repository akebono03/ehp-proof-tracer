$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_20.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_20.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py") `
  -Force

Write-Host "Phase 144-6-R5-20 parity audit files applied."
Write-Host "Added/replaced only:"
Write-Host "  audit_phase144_6_r5_20.py"
Write-Host "  tests/test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-20 targeted tests"
  Write-Host ("=" * 78)

  pytest -q `
    ".\tests\test_phase144_6_r5_18_production_generic_proof_chain_foundation.py" `
    ".\tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py" `
    ".\tests\test_phase144_6_r5_20_pi6_3_proof_chain_generic_parity.py"

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-20 parity audit"
  Write-Host ("=" * 78)

  python ".\audit_phase144_6_r5_20.py"

  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
