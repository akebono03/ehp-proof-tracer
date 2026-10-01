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
Write-Host "Phase 153-R11 Audit Path Repair R6"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/3] Compile audit"
Invoke-NativeChecked `
  -Label "py_compile" `
  -Command {
    python -m py_compile `
      "$PackageDir\audit_phase153_r11_audit_path_repair_r6.py"
  }

Write-Host ""
Write-Host "[2/3] Focused pytest confirmation"
Invoke-NativeChecked `
  -Label "focused pytest" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py"
  }

Write-Host ""
Write-Host "[3/3] R11 audit"
Invoke-NativeChecked `
  -Label "R11 audit" `
  -Command {
    python "$PackageDir\audit_phase153_r11_audit_path_repair_r6.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R11 Audit Path Repair R6 completed successfully."
Write-Host "Production changes: none."
Write-Host "Test changes: none."
Write-Host "Full test suite is intentionally NOT run here."
Write-Host "Punctuation normalization (, and .) remains deferred."
Write-Host "=============================================================="
