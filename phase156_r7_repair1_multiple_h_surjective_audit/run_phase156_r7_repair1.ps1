$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Split-Path -Parent $ScriptDir

Set-Location $RepoRoot

Write-Host "======================================================================================"
Write-Host "Phase156-R7 repair1 - multiple H-surjective ownership audit"
Write-Host "======================================================================================"
Write-Host "Repository root: $RepoRoot"
Write-Host "Production changes: none"
Write-Host ""

Write-Host "Current git HEAD:"
git rev-parse HEAD
Write-Host ""

Write-Host "[1/2] Read-only ownership audit"
python -m `
  phase156_r7_repair1_multiple_h_surjective_audit.audit_phase156_r7_repair1 `
  --output-dir ".\phase156_r7_repair1_audit_output"
Write-Host ""

Write-Host "[2/2] Existing focused regression tests"
python -m pytest `
  ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
  ".\tests\test_phase153_generic_concrete_proof_scope_recovery.py" `
  ".\tests\test_phase156_r5_repair13_root_reference_frontier.py" `
  ".\tests\test_phase156_r6_3_reason_prose_canonicalization.py" `
  -q
Write-Host ""

Write-Host "Repository-wide pytest is intentionally NOT run."
