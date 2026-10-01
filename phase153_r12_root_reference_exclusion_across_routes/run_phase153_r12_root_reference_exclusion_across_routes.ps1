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
Write-Host "Phase 153-R12 - Root Reference exclusion across routes"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Apply R12"
Invoke-NativeChecked `
  -Label "apply R12" `
  -Command {
    python "$PackageDir\apply_phase153_r12_root_reference_exclusion_across_routes.py"
  }

Write-Host ""
Write-Host "[2/4] Compile"
Invoke-NativeChecked `
  -Label "py_compile" `
  -Command {
    python -m py_compile `
      ".\toda_group_proof_narrative_references.py" `
      ".\toda_group_proof_narrative_contribution_renderer.py" `
      ".\toda_group_proof_narrative_renderer.py" `
      ".\tests\test_phase153_r12_root_reference_exclusion.py" `
      "$PackageDir\audit_phase153_r12_root_reference_exclusion_across_routes.py"
  }

Write-Host ""
Write-Host "[3/4] Focused pytest"
Invoke-NativeChecked `
  -Label "focused pytest" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase153_r8_reference_use_prose_normalization.py" `
      ".\tests\test_phase153_r9_reference_reuse_derivation_suppression.py" `
      ".\tests\test_phase153_r10_used_reference_filtering.py" `
      ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py" `
      ".\tests\test_phase153_r12_root_reference_exclusion.py"
  }

Write-Host ""
Write-Host "[4/4] R12 audit"
Invoke-NativeChecked `
  -Label "R12 audit" `
  -Command {
    python "$PackageDir\audit_phase153_r12_root_reference_exclusion_across_routes.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R12 focused verification completed successfully."
Write-Host "Full test suite is intentionally NOT run here."
Write-Host "Punctuation normalization (, and .) remains deferred."
Write-Host "=============================================================="
