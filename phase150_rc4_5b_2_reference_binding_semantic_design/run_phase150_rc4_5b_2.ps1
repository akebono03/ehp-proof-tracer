$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5B-2 Reference / variable-binding semantic design"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Design audit..."
  python `
    ".\phase150_rc4_5b_2_reference_binding_semantic_design\audit_phase150_rc4_5b_2.py"

  Write-Host ""
  Write-Host "B. Existing focused semantic tests..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase150_rc4_5_visible_reasons.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC4-5B-2 design completed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next: RC4-5B-3 minimal typed implementation."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
