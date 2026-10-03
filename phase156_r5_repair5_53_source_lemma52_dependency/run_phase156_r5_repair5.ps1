$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 repair5 - (5.3) source / Lemma 5.2 proof dependency"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/4] Apply repair5"
python -m phase156_r5_repair5_53_source_lemma52_dependency.apply_phase156_r5_repair5
Write-Host ""

Write-Host "[2/4] Focused repair5 tests"
python -m pytest `
  ".\tests\test_phase156_r5_repair5_53_source_lemma52_dependency.py" `
  -q
Write-Host ""

Write-Host "[3/4] Related regression tests"
python -m pytest `
  ".\tests\test_phase58_lemma52_specialization.py" `
  ".\tests\test_phase58_hopf_eta5_bridge.py" `
  ".\tests\test_phase144_6_r3_production_references.py" `
  ".\tests\test_phase150_rc4_4_reasons.py" `
  ".\tests\test_phase150_rc4_5_visible_reasons.py" `
  ".\tests\test_phase150_rc4_5b_3_reference_binding.py" `
  ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py" `
  ".\tests\test_phase156_r5_reference_attribution_separation.py" `
  ".\tests\test_phase156_r5_repair3_eta3_zero_attribution.py" `
  ".\tests\test_phase156_r5_repair4_bridge_reference_inference.py" `
  -q
Write-Host ""

Write-Host "[4/4] 112-group depth2/depth3 reaudit"
python -m `
  phase156_r5_repair5_53_source_lemma52_dependency.audit_phase156_r5_repair5 `
  --output-dir ".\phase156_r5_repair5_audit_output"
Write-Host ""

Write-Host "Repository-wide pytest is intentionally NOT run here."
