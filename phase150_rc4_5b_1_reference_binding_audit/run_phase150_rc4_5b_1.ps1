$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5B-1 Reference / beta->nu' binding audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_5b_1_reference_binding_audit\audit_phase150_rc4_5b_1.py"

  Write-Host ""
  Write-Host "B. Existing focused semantic tests..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase150_rc4_5_visible_reasons.py"

  Write-Host ""
  Write-Host "C. Reference / binding audit..."
  python `
    ".\phase150_rc4_5b_1_reference_binding_audit\audit_phase150_rc4_5b_1.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5B-1 audit completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
