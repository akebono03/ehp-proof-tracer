$ErrorActionPreference = "Stop"
Write-Host "=============================================================="
Write-Host "Phase 150 / RC4-5D-4"
Write-Host "order reason presentation-order audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="
$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"
try {
  Write-Host "`nA. Syntax preflight..."
  python -m py_compile ".\phase150_rc4_5d_4_order_reason_presentation_order_audit\audit_phase150_rc4_5d_4.py"

  Write-Host "`nB. Presentation-order audit..."
  python ".\phase150_rc4_5d_4_order_reason_presentation_order_audit\audit_phase150_rc4_5d_4.py"

  Write-Host "`nC. Related focused regression..."
  python -m pytest -q `
    ".\tests\test_phase150_rc4_5d_3_multiple_relation_to_order.py" `
    ".\tests\test_phase150_rc4_5c_2_exactness_to_map_property.py" `
    ".\tests\test_phase150_rc4_4_reasons.py" `
    ".\tests\test_phase149_rc3_4_ordering.py" `
    ".\tests\test_phase149_rc3_5_ordering_audit.py"

  Write-Host "`n=============================================================="
  Write-Host "RC4-5D-4 audit completed."
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
