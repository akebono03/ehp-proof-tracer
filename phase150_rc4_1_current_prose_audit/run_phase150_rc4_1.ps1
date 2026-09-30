$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-1 Current prose audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$Root = (Get-Location).Path
$env:PYTHONPATH = $Root
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_1_current_prose_audit\audit_phase150_rc4_1.py"

  Write-Host ""
  Write-Host "B. Focused related tests..."
  python -m pytest -q `
    ".\tests\test_phase134_9_pi6_3_snapshot.py" `
    ".\tests\test_phase142_3_generic_proof_text.py" `
    ".\tests\test_phase149_rc3_3_minimal_ordering.py"

  Write-Host ""
  Write-Host "C. Running RC4-1 audit..."
  python `
    ".\phase150_rc4_1_current_prose_audit\audit_phase150_rc4_1.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 150 / RC4-1 audit completed."
  Write-Host "No production files were changed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next: RC4-2 Reason-prose classification."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
