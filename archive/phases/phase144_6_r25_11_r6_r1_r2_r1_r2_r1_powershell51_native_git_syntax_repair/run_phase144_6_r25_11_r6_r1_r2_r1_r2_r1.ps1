$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$NewTestSource = Join-Path $RepairDir "payload\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py"
$NewTestTarget = Join-Path $TargetDir "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R1"
Write-Host "PowerShell 5.1 Native Git Syntax Repair"
Write-Host "Production changes: none"
Write-Host "Existing project test changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Transactional candidate generation and parser preflight..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File "$RepairDir\install_r25_11_r6_r1_r2_r1_r2_r1.ps1" `
    -RepoRoot $RepoRoot `
    -RepairDir $RepairDir

  $installExitCode = $LASTEXITCODE

  if ($installExitCode -ne 0) {
    throw "Transactional syntax repair failed with exit code $installExitCode"
  }

  Copy-Item `
    -Path $NewTestSource `
    -Destination $NewTestTarget `
    -Force

  Write-Host ""
  Write-Host "B. Focused audit-runner tests..."
  $env:PYTHONPATH = $RepoRoot

  pytest -q `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py"

  $testExitCode = $LASTEXITCODE
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($testExitCode -ne 0) {
    throw "Focused audit-runner tests failed with exit code $testExitCode"
  }

  Write-Host ""
  Write-Host "C. Resuming historical 190 localization..."

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
  Write-Host "R25-11-R6-R1-R2-R1-R2-R1 completed."
  Write-Host "No production files were modified."
  Write-Host "No existing project tests were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
