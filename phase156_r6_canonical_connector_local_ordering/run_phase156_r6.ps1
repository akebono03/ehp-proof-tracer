$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R6 - canonical expression / connector / local ordering"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/4] Apply Phase156-R6"
python -m phase156_r6_canonical_connector_local_ordering.apply_phase156_r6
Write-Host ""

Write-Host "[2/4] Focused Phase156-R6 tests"
python -m pytest `
  ".\tests\test_phase156_r6_canonical_connector_local_ordering.py" `
  ".\tests\test_phase156_r5_repair13_root_reference_frontier.py" `
  -q
Write-Host ""

Write-Host "[3/4] Related regression tests"
python -m pytest `
  ".\tests\test_phase143_57c_step_derivation_connector.py" `
  ".\tests\test_phase143_61b_direct_premise_narrative.py" `
  ".\tests\test_phase144_5_generic_definition_order_equations.py" `
  ".\tests\test_phase148_rc2_4_repair_r4_1_numbered_equation_dependency_audit.py" `
  ".\tests\test_phase148_rc2_4_repair_r4_2_calculation_premise_semantic_closure.py" `
  ".\tests\test_phase148_rc2_5_semantic_closure_scope.py" `
  ".\tests\test_phase150_rc4_5_visible_reasons.py" `
  ".\tests\test_phase156_r5_repair10_owned_step_line_suppression.py" `
  -q
Write-Host ""

Write-Host "[4/4] 112-group depth2/depth3 audit"
python -m `
  phase156_r6_canonical_connector_local_ordering.audit_phase156_r6 `
  --output-dir ".\phase156_r6_audit_output"
Write-Host ""

Write-Host "Repository-wide pytest is intentionally NOT run here."
