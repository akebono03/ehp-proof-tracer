$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5B-3-R1"
Write-Host "Repair legacy visible-reason expectation + beta LaTeX"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Applying the two minimal repairs..."
  python `
    ".\phase150_rc4_5b_3_r1_repair\apply_phase150_rc4_5b_3_r1.py"
  python `
    ".\phase150_rc4_5b_3_r1_repair\install_phase150_rc4_5b_3_r1_test.py"

  Write-Host ""
  Write-Host "B. Syntax preflight..."
  python -m py_compile `
    ".\toda_human_readable_renderer.py" `
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
  Write-Host "D. Visible Narrative audit..."
  python `
    ".\phase150_rc4_5b_3_r1_repair\audit_phase150_rc4_5b_3_r1.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5B-3-R1 completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next: confirm the actual Web Narrative."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
