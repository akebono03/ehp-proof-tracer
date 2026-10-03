$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 repair3 - eta_3 twice-zero attribution"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/4] Apply minimal repair3"
python -m phase156_r5_repair3_eta3_zero_attribution.apply_phase156_r5_repair3
Write-Host ""

Write-Host "[2/4] Focused repair3 tests"
python -m pytest `
  ".\tests\test_phase156_r5_repair3_eta3_zero_attribution.py" `
  -q
Write-Host ""

Write-Host "[3/4] Related existing / repair2 tests"
python -m pytest `
  ".\tests\test_phase58_lemma52_specialization.py" `
  ".\tests\test_phase144_6_r3_production_references.py" `
  ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py" `
  ".\tests\test_phase156_r5_reference_attribution_separation.py" `
  ".\tests\test_phase156_r5_repair2_lemma52_specialization_attribution.py" `
  -q
Write-Host ""

Write-Host "[4/4] 112-group attribution reaudit"
python -m `
  phase156_r5_repair3_eta3_zero_attribution.audit_phase156_r5_repair3 `
  --output-dir ".\phase156_r5_repair3_audit_output"
Write-Host ""

Write-Host "Repository-wide pytest is intentionally NOT run here."
