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
Write-Host "Phase 153-R7 Restore and Apply Recovery R2"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/6] Restore R7 pre-apply production files from backup"
Invoke-NativeChecked `
  -Label "restore pre-apply state" `
  -Command {
    python "$PackageDir\restore_phase153_r7_preapply_state.py"
  }

Write-Host ""
Write-Host "[2/6] Compile restored R6 production files before R7"
Invoke-NativeChecked `
  -Label "compile restored production files" `
  -Command {
    python -m py_compile `
      ".\toda_group_proof_narrative_contribution_renderer.py" `
      ".\toda_group_proof_narrative_renderer.py"
  }

Write-Host ""
Write-Host "[3/6] Apply corrected R7 patch"
Invoke-NativeChecked `
  -Label "apply corrected R7 patch" `
  -Command {
    python "$PackageDir\apply_phase153_r7.py"
  }

Write-Host ""
Write-Host "[4/6] Compile changed production files and R7 test/audit"
Invoke-NativeChecked `
  -Label "compile R7" `
  -Command {
    python -m py_compile `
      ".\toda_group_proof_narrative_contribution_renderer.py" `
      ".\toda_group_proof_narrative_renderer.py" `
      ".\tests\test_phase153_r7_proof_body_relevance.py" `
      "$PackageDir\audit_phase153_r7.py"
  }

Write-Host ""
Write-Host "[5/6] Focused pytest"
Invoke-NativeChecked `
  -Label "focused pytest" `
  -Command {
    python -m pytest -q `
      ".\tests\test_phase153_r5_reference_selection.py" `
      ".\tests\test_phase153_r6_reference_granularity.py" `
      ".\tests\test_phase153_r6_aggregate_component_granularity.py" `
      ".\tests\test_phase153_r7_proof_body_relevance.py" `
      ".\tests\test_phase144_6_r3_structured_references.py" `
      ".\tests\test_phase144_6_r3_production_references.py"
  }

Write-Host ""
Write-Host "[6/6] R7 representative-group audit"
Invoke-NativeChecked `
  -Label "representative-group audit" `
  -Command {
    python "$PackageDir\audit_phase153_r7.py"
  }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R7 Restore and Apply Recovery R2 completed successfully."
Write-Host "Full test suite is intentionally NOT run here."
Write-Host "=============================================================="
