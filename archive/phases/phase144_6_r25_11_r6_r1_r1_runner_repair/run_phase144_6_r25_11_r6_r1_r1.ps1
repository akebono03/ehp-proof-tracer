$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R1 runner repair installer"
Write-Host "Production changes: none"
Write-Host "Existing project test changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot
try {
  Write-Host ""
  Write-Host "A. Applying audit-runner-only repair..."
  python `
    ".\phase144_6_r25_11_r6_r1_r1_runner_repair\apply_r25_11_r6_r1_r1.py"

  if ($LASTEXITCODE -ne 0) {
    throw "Repair installer failed with exit code $LASTEXITCODE"
  }

  Write-Host ""
  Write-Host "B. Running repaired localization audit..."
  & powershell `
    -NoProfile `
    -ExecutionPolicy Bypass `
    -File ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\run_phase144_6_r25_11_r6_r1.ps1"

  $auditExitCode = $LASTEXITCODE
  if ($auditExitCode -ne 0) {
    throw "Repaired localization audit exited with code $auditExitCode"
  }
}
finally {
  Pop-Location
}
