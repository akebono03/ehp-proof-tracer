$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5D-1-R1"
Write-Host "Audit harness provenance import repair"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying audit-harness-only repair..."
  python `
    ".\phase150_rc4_5d_1_r1_audit_harness_repair\apply_phase150_rc4_5d_1_r1.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_5d_1_nu_prime_order_reason_audit\audit_phase150_rc4_5d_1.py"

  Write-Host ""
  Write-Host "C. Typed recursive reason-chain audit..."
  python `
    ".\phase150_rc4_5d_1_nu_prime_order_reason_audit\audit_phase150_rc4_5d_1.py"

  Write-Host ""
  Write-Host "D. Related focused regression..."
  python -m pytest -q `
    ".\tests\test_phase59_n3_ehp_chain.py" `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase150_rc4_5_visible_reasons.py" `
    ".\tests\test_phase150_rc4_5b_3_reference_binding.py" `
    ".\tests\test_phase150_rc4_5b_3_r1_beta_latex.py" `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5D-1-R1 audit completed."
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
