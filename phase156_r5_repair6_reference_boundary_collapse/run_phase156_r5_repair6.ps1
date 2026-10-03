$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 repair6 - Reference boundary collapse"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/4] Apply repair6"
python -m phase156_r5_repair6_reference_boundary_collapse.apply_phase156_r5_repair6
Write-Host ""

Write-Host "[2/4] Focused repair6 tests"
python -m pytest `
  ".\tests\test_phase156_r5_repair6_reference_boundary_collapse.py" `
  -q
Write-Host ""

Write-Host "[3/4] Related regression tests"
$tests = @(
  ".\tests\test_phase58_lemma52_specialization.py",
  ".\tests\test_phase58_hopf_eta5_bridge.py",
  ".\tests\test_phase144_6_r3_production_references.py",
  ".\tests\test_phase150_rc4_4_reasons.py",
  ".\tests\test_phase150_rc4_5_visible_reasons.py",
  ".\tests\test_phase150_rc4_5b_3_reference_binding.py",
  ".\tests\test_phase153_r3_5_reference_body_duplicate_suppression.py",
  ".\tests\test_phase153_r3_11_reference_body_ownership_repair.py",
  ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py",
  ".\tests\test_phase156_r5_reference_attribution_separation.py",
  ".\tests\test_phase156_r5_repair3_eta3_zero_attribution.py",
  ".\tests\test_phase156_r5_repair4_bridge_reference_inference.py"
)

if (Test-Path ".\tests\test_phase156_r5_repair2_lemma52_specialization_attribution.py") {
  $tests += ".\tests\test_phase156_r5_repair2_lemma52_specialization_attribution.py"
}

python -m pytest $tests -q
Write-Host ""

Write-Host "[4/4] 112-group depth2/depth3 audit"
python -m `
  phase156_r5_repair6_reference_boundary_collapse.audit_phase156_r5_repair6 `
  --output-dir ".\phase156_r5_repair6_audit_output"
Write-Host ""

Write-Host "Repository-wide pytest is intentionally NOT run here."
