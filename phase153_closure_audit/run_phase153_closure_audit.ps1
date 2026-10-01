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
Write-Host "Phase 153 Closure Audit"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/3] Compile audit"
Invoke-NativeChecked `
  -Label "compile audit" `
  -Command {
    python -m py_compile `
      "$PackageDir\audit_phase153_closure.py"
  }

Write-Host ""
Write-Host "[2/3] Phase 153 focused regression"
Invoke-NativeChecked `
  -Label "Phase 153 focused regression" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase153_r8_reference_use_prose_normalization.py" `
      ".\tests\test_phase153_r9_reference_reuse_derivation_suppression.py" `
      ".\tests\test_phase153_r10_used_reference_filtering.py" `
      ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py" `
      ".\tests\test_phase153_r12_root_reference_exclusion.py"
  }

Write-Host ""
Write-Host "[3/3] 112-group closure audit"
Invoke-NativeChecked `
  -Label "112-group closure audit" `
  -Command {
    python "$PackageDir\audit_phase153_closure.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153 Closure Audit completed successfully."
Write-Host "Production changes: none."
Write-Host "Full test suite is intentionally NOT run in this package."
Write-Host "If this passes, the next step is Phase 153 final full pytest."
Write-Host "Punctuation normalization (, and .) remains Phase 154 work."
Write-Host "=============================================================="
