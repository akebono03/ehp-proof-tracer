$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4 Closure Repair R1"
Write-Host "Filter reasons at the presentation visibility boundary"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying minimal production repair..."
  python ".\phase150_rc4_closure_repair_r1\apply_phase150_rc4_closure_repair_r1.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_group_proof_narrative_reasons.py" `
    ".\tests\test_phase150_rc4_closure_reason_visibility.py"

  Write-Host ""
  Write-Host "C. New cross-group visibility regression..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_closure_reason_visibility.py"

  Write-Host ""
  Write-Host "D. Existing focused RC4 regression..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
    ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase150_rc4_5f_2_final_group_structure_reason.py" `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py" `
    ".\tests\test_phase65_nu_prime_order_pi6_3.py"

  Write-Host ""
  Write-Host "E. Closure audit after repair..."
  python ".\phase150_rc4_closure_repair_r1\audit_phase150_rc4_closure_after_repair.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4 closure repair R1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
