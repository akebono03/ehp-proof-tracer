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
Write-Host "Phase 153-R5 Audit Launcher Repair R1"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/3] Compile repaired audit"
Invoke-NativeChecked `
  -Label "py_compile" `
  -Command {
    python -m py_compile `
      "$PackageDir\audit_phase153_r5.py"
  }

Write-Host ""
Write-Host "[2/3] Re-run Phase 153-R5 focused pytest"
Invoke-NativeChecked `
  -Label "focused pytest" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase153_r5_reference_selection.py" `
      ".\tests\test_phase144_6_r3_structured_references.py" `
      ".\tests\test_phase144_6_r3_production_references.py"
  }

Write-Host ""
Write-Host "[3/3] Re-run Phase 153-R5 representative-group audit"
Invoke-NativeChecked `
  -Label "representative-group audit" `
  -Command {
    python "$PackageDir\audit_phase153_r5.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R5 Audit Launcher Repair R1 completed successfully."
Write-Host "Full test suite is intentionally NOT run here."
Write-Host "=============================================================="
