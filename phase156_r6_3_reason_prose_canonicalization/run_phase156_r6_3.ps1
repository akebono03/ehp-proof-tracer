$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "=============================================================================="
Write-Host "Phase156-R6-3 - reason prose canonicalization"
Write-Host "=============================================================================="
Write-Host "Repository root: $RepoRoot"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/4] Apply R6-3"
python -m phase156_r6_3_reason_prose_canonicalization.apply_phase156_r6_3
Write-Host ""

Write-Host "[2/4] Focused R6-3 / R6 repair tests"
python -m pytest `
  ".\tests\test_phase156_r6_3_reason_prose_canonicalization.py" `
  ".\tests\test_phase156_r6_canonical_connector_local_ordering.py" `
  ".\tests\test_phase156_r6_repair1_relation_side_normalization.py" `
  ".\tests\test_phase156_r6_repair2_independent_relation_side_normalization.py" `
  -q
Write-Host ""

Write-Host "[3/4] Related regression tests"
python -m pytest `
  ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
  ".\tests\test_phase150_rc4_5_visible_reasons.py" `
  ".\tests\test_phase150_rc4_4_reasons.py" `
  ".\tests\test_phase143_57c_step_derivation_connector.py" `
  ".\tests\test_phase143_61b_direct_premise_narrative.py" `
  ".\tests\test_phase156_r5_repair13_root_reference_frontier.py" `
  -q
Write-Host ""

Write-Host "[4/4] 112-group depth2/depth3 audit"
python -m `
  phase156_r6_3_reason_prose_canonicalization.audit_phase156_r6_3 `
  --output-dir ".\phase156_r6_3_audit_output"
Write-Host ""

Write-Host "Repository-wide pytest is intentionally NOT run here."
