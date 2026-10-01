$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

function Invoke-NativeChecked {
  param(
    [Parameter(Mandatory = $true)]
    [scriptblock]$Command,
    [Parameter(Mandatory = $true)]
    [string]$Label
  )

  & $Command

  if ($LASTEXITCODE -ne 0) {
    throw "$Label failed with exit code $LASTEXITCODE."
  }
}

Write-Host "=============================================================="
Write-Host "Phase 153-R7 R5 Range Path Diagnostic"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/2] Compile diagnostic"
Invoke-NativeChecked `
  -Label "compile diagnostic" `
  -Command {
    python -m py_compile `
      "$PackageDir\diagnose_phase153_r7_range_paths_r5.py"
  }

Write-Host ""
Write-Host "[2/2] Inspect pi6_2 n>=6 paths to root"
Invoke-NativeChecked `
  -Label "R7 path diagnostic" `
  -Command {
    python "$PackageDir\diagnose_phase153_r7_range_paths_r5.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R7 R5 diagnostic completed."
Write-Host "Production changes: none."
Write-Host "Pytest: not run."
Write-Host "=============================================================="
