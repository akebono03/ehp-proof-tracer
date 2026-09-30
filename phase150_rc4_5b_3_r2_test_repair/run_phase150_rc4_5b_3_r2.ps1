$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5B-3-R2"
Write-Host "Repair beta LaTeX test expectation only"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying test-only repair..."
  python `
    ".\phase150_rc4_5b_3_r2_test_repair\apply_phase150_rc4_5b_3_r2.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\tests\test_phase150_rc4_5_visible_reasons.py" `
    ".\tests\test_phase150_rc4_5b_3_reference_binding.py" `
    ".\tests\test_phase150_rc4_5b_3_r1_beta_latex.py"

  Write-Host ""
  Write-Host "C. Focused tests..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase150_rc4_5_visible_reasons.py" `
    ".\tests\test_phase150_rc4_5b_3_reference_binding.py" `
    ".\tests\test_phase150_rc4_5b_3_r1_beta_latex.py"

  Write-Host ""
  Write-Host "D. Test expectation + visible prose audit..."
  python `
    ".\phase150_rc4_5b_3_r2_test_repair\audit_phase150_rc4_5b_3_r2.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5B-3-R2 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
