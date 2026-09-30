$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 149 RC3-4 Cross-group Ordering Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase149_rc3_4_cross_group_ordering_audit\audit_phase149_rc3_4.py" `
    ".\phase149_rc3_4_cross_group_ordering_audit\test_phase149_rc3_4_cross_group_ordering.py"

  Write-Host ""
  Write-Host "B. Running six-group ordering audit..."
  python `
    ".\phase149_rc3_4_cross_group_ordering_audit\audit_phase149_rc3_4.py" |
    Tee-Object `
      -FilePath ".\phase149_rc3_4_cross_group_ordering_audit\rc3_4_console_output.txt"

  Write-Host ""
  Write-Host "C. Installing RC3-4 audit tests..."
  Copy-Item `
    ".\phase149_rc3_4_cross_group_ordering_audit\test_phase149_rc3_4_cross_group_ordering.py" `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py" `
    -Force

  Write-Host ""
  Write-Host "D. Running RC3-4 + RC3-3 + RC2 focused regression..."
  pytest -q `
    ".\tests\test_phase149_rc3_4_cross_group_ordering.py" `
    ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
    ".\tests\test_phase148_rc2_4_cross_group_audit.py" `
    ".\tests\test_phase148_rc2_4_post_repair_six_group.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "RC3-4 audit run completed."
  Write-Host "Production changes: none"
  Write-Host "Repository-wide tests remain deferred to RC3-5."
  Write-Host "Review audit_output\summary.txt and six narrative files."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
