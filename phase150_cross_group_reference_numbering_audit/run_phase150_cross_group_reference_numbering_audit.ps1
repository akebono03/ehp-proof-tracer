$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 Cross-Group Reference Numbering Audit"
Write-Host "Production changes: none"
Write-Host "Existing test changes: none"
Write-Host "=============================================================="

$repoRoot = (Get-Location).Path
$testsPath = Join-Path $repoRoot "tests"
$env:PYTHONPATH = "$repoRoot;$testsPath"
$env:PYTHONIOENCODING = "utf-8"

try {
  Write-Host ""
  Write-Host "A. Syntax preflight..."
  python -m py_compile `
    ".\phase150_cross_group_reference_numbering_audit\audit_phase150_cross_group_reference_numbering.py"

  Write-Host ""
  Write-Host "B. Cross-group Reference numbering audit..."
  python `
    ".\phase150_cross_group_reference_numbering_audit\audit_phase150_cross_group_reference_numbering.py"

  Write-Host ""
  Write-Host "C. Existing Reference/Narrative focused regression..."
  python -m pytest -q `
    ".\tests\test_phase144_5_generic_definition_order_equations.py" `
    ".\tests\test_phase150_rc4_5f_2_final_group_structure_reason.py" `
    ".\tests\test_phase150_rc4_closure_reason_visibility.py"

  Write-Host ""
  Write-Host "=============================================================="
  Write-Host "Cross-group Reference numbering audit completed."
  Write-Host "Production changes: none"
  Write-Host "Existing test changes: none"
  Write-Host "Repository-wide tests were intentionally not run."
  Write-Host "=============================================================="
}
finally {
  Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
  Remove-Item Env:PYTHONIOENCODING -ErrorAction SilentlyContinue
}
