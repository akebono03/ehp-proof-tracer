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
Write-Host "Phase 153 Final Regression"
Write-Host "Stale Phase 132 CLI Test Repair R1"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/3] Apply test-only repair"
Invoke-NativeChecked `
  -Label "apply test-only repair" `
  -Command {
    python "$PackageDir\apply_phase153_final_regression_stale_phase132_cli_test_repair_r1.py"
  }

Write-Host ""
Write-Host "[2/3] Compile updated test"
Invoke-NativeChecked `
  -Label "compile updated test" `
  -Command {
    python -m py_compile `
      ".\tests\test_phase132_7_group_proof_cli_modes.py"
  }

Write-Host ""
Write-Host "[3/3] Focused regression"
Invoke-NativeChecked `
  -Label "focused regression" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase132_7_group_proof_cli_modes.py" `
      ".\tests\test_phase145_group_proof_defaults.py" `
      ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py" `
      ".\tests\test_phase153_r12_root_reference_exclusion.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Focused repair verification passed."
Write-Host "Production changes: none."
Write-Host "Next: python -m pytest .\tests -x"
Write-Host "=============================================================="
