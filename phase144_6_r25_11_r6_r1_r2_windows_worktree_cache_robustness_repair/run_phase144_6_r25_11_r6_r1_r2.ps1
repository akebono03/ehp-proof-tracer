$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path `
  $RepoRoot `
  "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path `
  $TargetDir `
  "locate_historical_190.ps1"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2 Windows Worktree/Cache Robustness Repair"
Write-Host "Production changes: none"
Write-Host "Existing project test changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot
try {
  Write-Host ""
  Write-Host "A. Applying audit-only robustness repair..."
  python `
    ".\phase144_6_r25_11_r6_r1_r2_windows_worktree_cache_robustness_repair\apply_r25_11_r6_r1_r2.py"

  if ($LASTEXITCODE -ne 0) {
    throw (
      "R2 repair installer failed with exit code " +
      "$LASTEXITCODE"
    )
  }

  Write-Host ""
  Write-Host "B. PowerShell parser preflight..."
  $parseErrors = $null
  $parseTokens = $null

  [void][System.Management.Automation.Language.Parser]::ParseFile(
    $Locator,
    [ref]$parseTokens,
    [ref]$parseErrors
  )

  if ($parseErrors.Count -ne 0) {
    foreach ($parseError in $parseErrors) {
      Write-Host $parseError.Message
    }
    throw "PowerShell parser preflight failed."
  }

  Write-Host "PowerShell parser preflight: PASS"

  Write-Host ""
  Write-Host "C. Focused robustness tests..."
  $env:PYTHONPATH = $RepoRoot
  pytest -q `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2.py"

  $testExitCode = $LASTEXITCODE
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue

  if ($testExitCode -ne 0) {
    throw (
      "Focused robustness tests failed with exit code " +
      "$testExitCode"
    )
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
    throw (
      "Historical 190 localization stopped with exit code " +
      "$localizationExitCode"
    )
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R25-11-R6-R1-R2 completed."
  Write-Host "Existing population cache was reused."
  Write-Host "No production files were modified."
  Write-Host "No existing project tests were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH `
    -ErrorAction SilentlyContinue
  Pop-Location
}
