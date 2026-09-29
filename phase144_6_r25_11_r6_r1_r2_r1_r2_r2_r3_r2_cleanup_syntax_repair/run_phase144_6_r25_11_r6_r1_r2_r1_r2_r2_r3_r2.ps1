$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$Installer = Join-Path $RepairDir "install_r25_11_r6_r1_r2_r1_r2_r2_r3.ps1"
$Cleanup = Join-Path $RepairDir "cleanup_verified_a2d9_worktrees.ps1"
$NewTestSource = Join-Path $RepairDir "payload\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py"
$NewTestTarget = Join-Path $TargetDir "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3.py"

function Assert-PowerShellParses {
  param(
    [Parameter(Mandatory=$true)]
    [string]$Path,

    [Parameter(Mandatory=$true)]
    [string]$Label
  )

  $parseErrors = $null
  $parseTokens = $null

  [void][System.Management.Automation.Language.Parser]::ParseFile(
    $Path,
    [ref]$parseTokens,
    [ref]$parseErrors
  )

  if ($parseErrors.Count -ne 0) {
    foreach ($parseError in $parseErrors) {
      Write-Host $parseError.Message
    }

    throw "$Label parser preflight failed."
  }

  Write-Host "$Label parser preflight: PASS"
}

Write-Host "=============================================================="
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R2"
Write-Host "Cleanup Syntax Repair"
Write-Host "Production changes: none"
Write-Host "Locator payload changes from R3: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Parser preflight for repair scripts..."
  Assert-PowerShellParses -Path $Installer -Label "Installer"
  Assert-PowerShellParses -Path $Cleanup -Label "Cleanup"

  Write-Host ""
  Write-Host "B. Installing unchanged R3 scalar exit-code repair..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $Installer `
    -RepoRoot $RepoRoot `
    -RepairDir $RepairDir

  if ($LASTEXITCODE -ne 0) {
    throw "Scalar exit-code repair installation failed."
  }

  Copy-Item -Path $NewTestSource -Destination $NewTestTarget -Force

  Write-Host ""
  Write-Host "C. Cleaning only verified residual a2d9a492 worktrees..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $Cleanup `
    -RepoRoot $RepoRoot

  if ($LASTEXITCODE -ne 0) {
    throw "Verified residual worktree cleanup failed."
  }

  Write-Host ""
  Write-Host "D. Focused historical-localization tests..."
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
  Write-Host "E. Resuming historical 190 localization..."

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
  Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R3-R2 completed."
  Write-Host "No production files were modified."
  Write-Host "No existing project tests were modified."
  Write-Host "No full pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
