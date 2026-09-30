$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-3 General rule design"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_rc4_3_general_rule_design\audit_phase150_rc4_3.py"

  Write-Host ""
  Write-Host "B. Focused architecture tests..."
  python -m pytest -q `
    ".\tests\test_phase143_19_method_evidence.py" `
    ".\tests\test_phase144_6_r5_42_generic_narrative_contribution_production_foundation.py" `
    ".\tests\test_phase149_rc3_3_minimal_ordering.py"

  Write-Host ""
  Write-Host "C. Running RC4-3 design audit..."
  python `
    ".\phase150_rc4_3_general_rule_design\audit_phase150_rc4_3.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Phase 150 / RC4-3 design audit completed."
  Write-Host "No production files were changed."
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "Next: RC4-4 Minimal implementation."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
