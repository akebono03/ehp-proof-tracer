$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5F-1-R1"
Write-Host "Final group-structure audit import repair"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Repairing audit-harness import..."
  python `
    ".\phase150_rc4_5f_1_r1_audit_import_repair\apply_phase150_rc4_5f_1_r1.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_5f_1_final_group_structure_reason_chain_audit\audit_phase150_rc4_5f_1.py"

  Write-Host ""
  Write-Host "C. Re-running final group-structure typed evidence audit..."
  python `
    ".\phase150_rc4_5f_1_final_group_structure_reason_chain_audit\audit_phase150_rc4_5f_1.py"

  Write-Host ""
  Write-Host "D. Related focused regression..."
  python -m pytest -q `
    ".\tests\test_phase143_2_generic_short_exact_sequence.py" `
    ".\tests\test_phase143_42_argument_body_contribution_renderer.py" `
    ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5F-1-R1 completed."
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
