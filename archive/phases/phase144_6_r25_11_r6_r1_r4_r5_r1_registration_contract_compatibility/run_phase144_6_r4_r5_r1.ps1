$ErrorActionPreference = "Stop"

$RepairDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $RepairDir
$TargetDir = Join-Path $RepoRoot "phase144_6_r25_11_r6_r1_historical_190_commit_localization_audit"
$Locator = Join-Path $TargetDir "locate_historical_190.ps1"
$Installer = Join-Path $RepairDir "install_r4_r5_r1.ps1"
$TestSource = Join-Path $RepairDir "payload\test_phase144_6_r4_r5_r1.py"
$TestTarget = Join-Path $TargetDir "test_phase144_6_r4_r5_r1.py"

Write-Host "=============================================================="
Write-Host "Phase 144-6 R4-R5-R1 Registration Contract Compatibility"
Write-Host "Known exact baseline: 39a1b8bfad = 190"
Write-Host "Production changes: none"
Write-Host "=============================================================="

Push-Location $RepoRoot

try {
  Write-Host ""
  Write-Host "A. Installing compatibility repair..."
  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $Installer `
    -RepoRoot $RepoRoot

  if ($LASTEXITCODE -ne 0) {
    throw "R4-R5-R1 installation failed."
  }

  Copy-Item -Path $TestSource -Destination $TestTarget -Force

  Write-Host ""
  Write-Host "B. Running focused historical-localization tests..."
  $env:PYTHONPATH = $RepoRoot
  pytest -q $TargetDir
  $testExitCode = $LASTEXITCODE
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

  if ($testExitCode -ne 0) {
    throw "Focused historical-localization tests failed with exit code $testExitCode"
  }

  Write-Host ""
  Write-Host "C. Resuming historical localization..."
  & powershell `
    -NoProfile `
    -NonInteractive `
    -ExecutionPolicy Bypass `
    -File $Locator `
    -RepoRoot $RepoRoot `
    -PhaseDir $TargetDir

  $localizationExitCode = $LASTEXITCODE

  if ($localizationExitCode -ne 0) {
    throw "Historical localization stopped with exit code $localizationExitCode"
  }

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "R4-R5-R1 completed."
  Write-Host "Inspect the first selected=192 after 39a1b8bfad."
  Write-Host "No production files were modified."
  Write-Host "No full project pytest was run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Pop-Location
}
