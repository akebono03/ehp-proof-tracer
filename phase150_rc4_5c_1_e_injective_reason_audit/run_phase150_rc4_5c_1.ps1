$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5C-1"
Write-Host "E injective reason-chain audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_5c_1_e_injective_reason_audit\audit_phase150_rc4_5c_1.py"

  Write-Host ""
  Write-Host "B. Existing related focused tests..."
  python -m pytest -q `
    ".\tests\test_phase59_n3_ehp_chain.py" `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase150_rc4_5_visible_reasons.py" `
    ".\tests\test_phase150_rc4_5b_3_reference_binding.py" `
    ".\tests\test_phase150_rc4_5b_3_r1_beta_latex.py"

  Write-Host ""
  Write-Host "C. Typed premise audit..."
  python `
    ".\phase150_rc4_5c_1_e_injective_reason_audit\audit_phase150_rc4_5c_1.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5C-1 audit completed."
  Write-Host "Production changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
