$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

Copy-Item `
  -Path (Join-Path $PackageDir "payload\audit_phase144_6_r5_17a.py") `
  -Destination (Join-Path $RepoRoot "audit_phase144_6_r5_17a.py") `
  -Force

Copy-Item `
  -Path (Join-Path $PackageDir "payload\tests\test_phase144_6_r5_17a_proof_chain_selection_audit.py") `
  -Destination (Join-Path $RepoRoot "tests\test_phase144_6_r5_17a_proof_chain_selection_audit.py") `
  -Force

Write-Host "Phase 144-6-R5-17A audit files applied."
Write-Host "Added/replaced only:"
Write-Host "  audit_phase144_6_r5_17a.py"
Write-Host "  tests/test_phase144_6_r5_17a_proof_chain_selection_audit.py"
