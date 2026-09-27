$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\toda_group_proof_narrative_proof_chains.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_proof_chains.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_18_production_generic_proof_chain_foundation.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_18_production_generic_proof_chain_foundation.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_18.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_18.py") `
  -Force

Write-Host "Phase 144-6-R5-18 production foundation applied."
Write-Host "Added/replaced only:"
Write-Host "  toda_group_proof_narrative_proof_chains.py"
Write-Host "  tests/test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"
Write-Host "  audit_phase144_6_r5_18.py"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-18 targeted tests"
  Write-Host ("=" * 78)
  pytest -q `
    ".\tests\test_phase144_6_r5_18_production_generic_proof_chain_foundation.py"

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-18 production ProofChain audit"
  Write-Host ("=" * 78)
  python ".\audit_phase144_6_r5_18.py"

  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
