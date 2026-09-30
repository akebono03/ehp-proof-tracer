$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-2 Reason-prose classification"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_2_reason_prose_classification\audit_phase150_rc4_2.py"

  Write-Host ""
  Write-Host "B. Focused semantic tests..."
  python -m pytest -q `
    ".\tests\test_phase141_narrative_blocks.py" `
    ".\tests\test_phase143_19_method_evidence.py" `
    ".\tests\test_phase149_rc3_3_minimal_ordering.py"

  Write-Host ""
  Write-Host "C. Running RC4-2 classification audit..."
  python `
    ".\phase150_rc4_2_reason_prose_classification\audit_phase150_rc4_2.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 150 / RC4-2 classification completed."
  Write-Host "No production files were changed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next: RC4-3 General rule design."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
