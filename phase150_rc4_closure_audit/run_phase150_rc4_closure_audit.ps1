$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4 Closure Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_closure_audit\audit_phase150_rc4_closure.py"

  Write-Host ""
  Write-Host "B. RC4 closure audit..."
  python `
    ".\phase150_rc4_closure_audit\audit_phase150_rc4_closure.py"

  Write-Host ""
  Write-Host "C. Focused Phase 150 regression..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
    ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase150_rc4_5f_2_final_group_structure_reason.py" `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py" `
    ".\tests\test_phase65_nu_prime_order_pi6_3.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 150 RC4 closure audit completed."
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
