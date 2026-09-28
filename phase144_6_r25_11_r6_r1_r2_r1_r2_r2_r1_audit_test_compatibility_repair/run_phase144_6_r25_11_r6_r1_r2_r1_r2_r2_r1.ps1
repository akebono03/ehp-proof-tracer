$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R1"
Write-Host "Audit Test Compatibility Repair"
Write-Host "Production changes: none"
Write-Host "Locator changes: none"
Write-Host "Existing project test changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Applying audit-test-only compatibility repair..."

  python ".\phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r1_audit_test_compatibility_repair\apply_r25_11_r6_r1_r2_r1_r2_r2_r1.py"

  $applyExitCode = $LASTEXITCODE

  if ($applyExitCode -ne 0) {
    throw "Audit test compatibility repair failed with exit code $applyExitCode"
  }

  Write-Host ""
  Write-Host "B. Confirming installed locator still parses..."
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

    throw "Installed locator parser preflight failed."
  }

  Write-Host "Installed locator PowerShell parser preflight: PASS"

  Write-Host ""
  Write-Host "C. Focused audit-runner tests..."
  $env:PYTHONPATH = $RepoRoot

  pytest -q `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1.py" `
    ".\phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r1_r2_r2.py"

  $testExitCode = $LASTEXITCODE
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($testExitCode -ne 0) {
    throw "Focused audit-runner tests failed with exit code $testExitCode"
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
  Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R1 completed."
  Write-Host "No production files were modified."
  Write-Host "No locator files were modified."
  Write-Host "No existing project tests were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
