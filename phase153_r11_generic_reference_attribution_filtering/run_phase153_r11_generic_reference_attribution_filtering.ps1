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
Write-Host "Phase 153-R11 - Generic-route Reference attribution/filtering"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Apply R11"
Invoke-NativeChecked `
  -Label "apply R11" `
  -Command {
    python "$PackageDir\apply_phase153_r11_generic_reference_attribution_filtering.py"
  }

Write-Host ""
Write-Host "[2/4] Compile"
Invoke-NativeChecked `
  -Label "py_compile" `
  -Command {
    python -m py_compile `
      ".\toda_group_proof_narrative_references.py" `
      ".\toda_group_proof_narrative_contribution_renderer.py" `
      ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py" `
      "$PackageDir\audit_phase153_r11_generic_reference_attribution_filtering.py"
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
      ".\tests\test_phase144_6_r3_structured_references.py" `
      ".\tests\test_phase144_6_r3_production_references.py" `
      ".\tests\test_phase143_46_multi_argument_narrative_assembler.py" `
      ".\tests\test_phase143_47_multi_argument_shared_contribution_dedup.py"
  }

Write-Host ""
Write-Host "[4/4] Generic-route audit"
Invoke-NativeChecked `
  -Label "generic-route audit" `
  -Command {
    python "$PackageDir\audit_phase153_r11_generic_reference_attribution_filtering.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R11 focused verification completed successfully."
Write-Host "Full test suite is intentionally NOT run here."
Write-Host "Punctuation normalization (, and .) is intentionally deferred."
Write-Host "=============================================================="
