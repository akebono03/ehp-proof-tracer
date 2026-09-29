$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$NewTestSource = Join-Path $RepairDir "payload\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py"
$NewTestTarget = Join-Path $TargetDir "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3"
Write-Host "Native Command Scalar Exit-Code Repair"
Write-Host "Production changes: none"
Write-Host "Existing project test changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Installing scalar exit-code repair transactionally..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File "$RepairDir\install_r25_11_r6_r1_r2_r1_r2_r2_r3.ps1" `
    -RepoRoot $RepoRoot `
    -RepairDir $RepairDir

  if ($LASTEXITCODE -ne 0) {
    throw "Scalar exit-code repair installation failed."
  }

  Copy-Item -Path $NewTestSource -Destination $NewTestTarget -Force

  Write-Host ""
  Write-Host "B. Cleaning only verified residual a2d9a492 worktrees..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File "$RepairDir\cleanup_verified_a2d9_worktrees.ps1" `
    -RepoRoot $RepoRoot

  if ($LASTEXITCODE -ne 0) {
    throw "Verified residual worktree cleanup failed."
  }

  Write-Host ""
  Write-Host "C. Focused historical-localization tests..."
  $env:PYTHONPATH = $RepoRoot

  pytest -q `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_r2_r2.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py"

  $testExitCode = $LASTEXITCODE
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($testExitCode -ne 0) {
    throw "Focused historical-localization tests failed with exit code $testExitCode"
  }

  Write-Host ""
  Write-Host "D. Resuming historical 190 localization..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $Locator `
    -RepoRoot $RepoRoot `
    -PhaseDir $TargetDir

  $localizationExitCode = $LASTEXITCODE

  if ($localizationExitCode -ne 0) {
    throw "Historical 190 localization stopped with exit code $localizationExitCode"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R3 completed."
  Write-Host "No production files were modified."
  Write-Host "No existing project tests were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
