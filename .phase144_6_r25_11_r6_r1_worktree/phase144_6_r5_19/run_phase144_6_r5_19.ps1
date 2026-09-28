$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Copy-Item `
  -Path (Join-Path $PackageDir "payload\toda_group_proof_narrative_proof_chain_renderer.py") `
  -Destination (Join-Path $RepoRoot "toda_group_proof_narrative_proof_chain_renderer.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_19.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_19.py") `
  -Force

Write-Host "Phase 144-6-R5-19 ProofChain Narrative integration applied."
Write-Host "Added/replaced only:"
Write-Host "  toda_group_proof_narrative_proof_chain_renderer.py"
Write-Host "  tests/test_phase144_6_r5_19_proof_chain_narrative_integration.py"
Write-Host "  audit_phase144_6_r5_19.py"

Push-Location $RepoRoot
try {
  $env:PYTHONPATH = (Get-Location).Path

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-19 targeted tests"
  Write-Host ("=" * 78)

  pytest -q `
    ".\tests\test_phase144_6_r5_18_production_generic_proof_chain_foundation.py" `
    ".\tests\test_phase144_6_r5_19_proof_chain_narrative_integration.py"

  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ("=" * 78)
  Write-Host "Phase 144-6-R5-19 integration audit"
  Write-Host ("=" * 78)

  python ".\audit_phase144_6_r5_19.py"

  exit $LASTEXITCODE
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
