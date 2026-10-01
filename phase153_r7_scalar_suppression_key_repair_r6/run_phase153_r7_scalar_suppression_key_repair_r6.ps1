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
Write-Host "Phase 153-R7 Scalar Suppression-Key Repair R6"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Apply R7 repair"
Invoke-NativeChecked `
  -Label "apply R7 R6 repair" `
  -Command {
    python "$PackageDir\apply_phase153_r7_scalar_suppression_key_repair_r6.py"
  }

Write-Host ""
Write-Host "[2/4] Compile"
Invoke-NativeChecked `
  -Label "py_compile" `
  -Command {
    python -m py_compile `
      ".\toda_group_proof_narrative_contribution_renderer.py" `
      ".\toda_group_proof_narrative_renderer.py" `
      ".\tests\test_phase153_r7_proof_body_relevance.py" `
      ".\tests\test_phase153_r7_independent_root_path.py" `
      ".\tests\test_phase153_r7_sibling_boundary.py" `
      ".\tests\test_phase153_r7_scalar_suppression_key.py" `
      "$PackageDir\audit_phase153_r7_scalar_suppression_key_repair_r6.py"
  }

Write-Host ""
Write-Host "[3/4] Focused pytest"
Invoke-NativeChecked `
  -Label "focused pytest" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase153_r5_reference_selection.py" `
      ".\tests\test_phase153_r6_reference_granularity.py" `
      ".\tests\test_phase153_r6_aggregate_component_granularity.py" `
      ".\tests\test_phase153_r7_proof_body_relevance.py" `
      ".\tests\test_phase153_r7_independent_root_path.py" `
      ".\tests\test_phase153_r7_sibling_boundary.py" `
      ".\tests\test_phase153_r7_scalar_suppression_key.py" `
      ".\tests\test_phase144_6_r3_structured_references.py" `
      ".\tests\test_phase144_6_r3_production_references.py"
  }

Write-Host ""
Write-Host "[4/4] Representative audit"
Invoke-NativeChecked `
  -Label "representative audit" `
  -Command {
    python "$PackageDir\audit_phase153_r7_scalar_suppression_key_repair_r6.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R7 Scalar Suppression-Key Repair R6 completed successfully."
Write-Host "Full test suite is intentionally NOT run here."
Write-Host "=============================================================="
