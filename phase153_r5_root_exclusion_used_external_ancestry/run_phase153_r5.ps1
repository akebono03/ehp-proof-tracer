$ErrorActionPreference = "Stop"

$PackageDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $PackageDir

Write-Host "=============================================================="
Write-Host "Phase 153-R5 - root exclusion + used external ancestry"
Write-Host "=============================================================="

Set-Location $RepoRoot

Write-Host ""
Write-Host "[1/4] Apply patch"
python "$PackageDir\apply_phase153_r5.py"

Write-Host ""
Write-Host "[2/4] Compile changed production files and R5 test/audit"
python -m py_compile `
  ".\toda_group_proof_narrative_references.py" `
  ".\toda_group_proof_narrative_contribution_renderer.py" `
  ".\tests\test_phase153_r5_reference_selection.py" `
  "$PackageDir\audit_phase153_r5.py"

Write-Host ""
Write-Host "[3/4] Focused pytest"
python -m pytest -q `
  ".\tests\test_phase153_r5_reference_selection.py" `
  ".\tests\test_phase144_6_r3_structured_references.py" `
  ".\tests\test_phase144_6_r3_production_references.py"

Write-Host ""
Write-Host "[4/4] R5 representative-group audit"
python "$PackageDir\audit_phase153_r5.py"

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 153-R5 focused verification completed."
Write-Host "Full test suite is intentionally NOT run here."
Write-Host "=============================================================="
