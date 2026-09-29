$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = (Get-Location).Path

powershell -ExecutionPolicy Bypass `
  -File (Join-Path $PackageDir "apply_phase144_6_r5_17a.ps1")

$env:PYTHONPATH = $RepoRoot
try {
  Write-Host "=============================================================================="
  Write-Host "Phase 144-6-R5-17A targeted tests"
  Write-Host "=============================================================================="
  pytest -q ".\tests\test_phase144_6_r5_17a_proof_chain_selection_audit.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }

  Write-Host ""
  Write-Host "=============================================================================="
  Write-Host "Phase 144-6-R5-17A pi_6^3 proof-chain audit"
  Write-Host "=============================================================================="
  python ".\audit_phase144_6_r5_17a.py"
  if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
  }
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
}
