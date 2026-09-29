$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$Installer = Join-Path $RepairDir "install_read_population_cache_restoration.ps1"
$TestSource = Join-Path $RepairDir "payload\test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_r2.py"
$TestTarget = Join-Path $TargetDir "test_phase144_6_r25_11_r6_r1_r2_r1_r2_r2_r3_r4_r2.py"

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
Write-Host "Phase 144-6 R25-11-R6-R1-R2-R1-R2-R2-R3-R4-R2"
Write-Host "Read-PopulationCache Restoration Repair"
Write-Host "Production changes: none"
Write-Host "Measure-Commit changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Parser preflight..."
  Assert-PowerShellParses -Path $Installer -Label "Installer"

  Write-Host ""
  Write-Host "B. Restoring original Read-PopulationCache helper..."

  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $Installer `
    -RepoRoot $RepoRoot `
    -RepairDir $RepairDir

  if ($LASTEXITCODE -ne 0) {
    throw "Read-PopulationCache restoration failed."
  }

  Copy-Item -Path $TestSource -Destination $TestTarget -Force

  Write-Host ""
  Write-Host "C. Running focused historical-localization audit directory..."
  $env:PYTHONPATH = $RepoRoot

  pytest -q $TargetDir

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
  Write-Host "R25-11-R6-R1-R2-R1-R2-R2-R3-R4-R2 completed."
  Write-Host "No production files were modified."
  Write-Host "No full project pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
