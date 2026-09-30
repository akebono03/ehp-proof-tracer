$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5D-2"
Write-Host "order-four semantic sufficiency audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_5d_2_order_four_semantic_sufficiency_audit\audit_phase150_rc4_5d_2.py"

  Write-Host ""
  Write-Host "B. Typed semantic sufficiency audit..."
  python `
    ".\phase150_rc4_5d_2_order_four_semantic_sufficiency_audit\audit_phase150_rc4_5d_2.py"

  Write-Host ""
  Write-Host "C. Related focused regression..."
  python -m pytest -q `
    ".\tests\test_phase65_nu_prime_order_pi6_3.py" `
    ".\tests\test_phase59_n3_ehp_chain.py" `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase150_rc4_5_visible_reasons.py" `
    ".\tests\test_phase150_rc4_5b_3_reference_binding.py" `
    ".\tests\test_phase150_rc4_5b_3_r1_beta_latex.py" `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5D-2 audit completed."
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
