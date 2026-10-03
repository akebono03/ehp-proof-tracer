$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R5 repair12 - Reference frontier"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/4] Apply repair12"
python -m phase156_r5_repair12_reference_frontier.apply_phase156_r5_repair12
Write-Host ""

Write-Host "[2/4] Focused repair11/12 tests"
python -m pytest `
  ".\tests\test_phase156_r5_repair11_reference_dependency_pruning.py" `
  ".\tests\test_phase156_r5_repair12_reference_frontier.py" `
  -q
Write-Host ""

Write-Host "[3/4] Related regression tests"
$tests = @(
  ".\tests\test_phase144_6_r3_production_references.py",
  ".\tests\test_phase150_rc4_5_visible_reasons.py",
  ".\tests\test_phase153_r3_5_reference_body_duplicate_suppression.py",
  ".\tests\test_phase153_r3_11_reference_body_ownership_repair.py",
  ".\tests\test_phase153_r11_generic_reference_attribution_filtering.py",
  ".\tests\test_phase156_r5_reference_attribution_separation.py",
  ".\tests\test_phase156_r5_repair3_eta3_zero_attribution.py",
  ".\tests\test_phase156_r5_repair4_bridge_reference_inference.py",
  ".\tests\test_phase156_r5_repair6_reference_boundary_collapse.py",
  ".\tests\test_phase156_r5_repair7_reference_boundary_filter_order.py",
  ".\tests\test_phase156_r5_repair8_reference_owned_ancestor_closure.py",
  ".\tests\test_phase156_r5_repair9_test_contract_after_boundary_collapse.py",
  ".\tests\test_phase156_r5_repair10_owned_step_line_suppression.py"
)

if (Test-Path ".\tests\test_phase156_r5_repair2_lemma52_specialization_attribution.py") {
  $tests += ".\tests\test_phase156_r5_repair2_lemma52_specialization_attribution.py"
}

python -m pytest $tests -q
Write-Host ""

Write-Host "[4/4] 112-group depth2/depth3 audit"
python -m `
  phase156_r5_repair12_reference_frontier.audit_phase156_r5_repair12 `
  --output-dir ".\phase156_r5_repair12_audit_output"
Write-Host ""

Write-Host "Repository-wide pytest is intentionally NOT run here."
