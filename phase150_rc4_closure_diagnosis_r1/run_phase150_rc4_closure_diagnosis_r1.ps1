$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4 Closure Diagnosis R1"
Write-Host "Target: pi_10^4"
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
    ".\phase150_rc4_closure_diagnosis_r1\diagnose_phase150_rc4_closure_r1.py"

  Write-Host ""
  Write-Host "B. Diagnosing pi_10^4 reason/presentation boundary..."
  python `
    ".\phase150_rc4_closure_diagnosis_r1\diagnose_phase150_rc4_closure_r1.py"

  Write-Host ""
  Write-Host "C. Existing focused regression remains unchanged..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
    ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
    ".\tests\test_phase150_rc4_5e_2_short_exact_derivation_reason.py" `
    ".\tests\test_phase150_rc4_5f_2_final_group_structure_reason.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4 closure diagnosis R1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
