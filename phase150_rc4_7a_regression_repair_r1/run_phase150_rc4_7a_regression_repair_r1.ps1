$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7A Regression Repair R1"
Write-Host "Reference provenance / mathematical-content separation"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "A. Applying minimal production repair..."
python ".\phase150_rc4_7a_regression_repair_r1\apply_phase150_rc4_7a_regression_repair_r1.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\toda_group_proof_narrative_argument_multi_renderer.py" `
  ".\toda_group_proof_narrative_contribution_renderer.py" `
  ".\phase150_rc4_7a_regression_repair_r1\test_phase150_rc4_7a_regression_repair_r1.py"

Write-Host ""
Write-Host "C. New focused regression tests..."
python -m pytest -q `
  ".\phase150_rc4_7a_regression_repair_r1\test_phase150_rc4_7a_regression_repair_r1.py"

Write-Host ""
Write-Host "D. Phase 148 exactness regressions..."
python -m pytest -q `
  ".\tests\test_phase148_rc2_4_repair_r5.py" `
  ".\tests\test_phase148_rc2_4_repair_r5_r2.py"

Write-Host ""
Write-Host "E. Phase 143 low-level multi-Argument regression..."
python -m pytest -q `
  ".\tests\test_phase143_46_multi_argument_narrative_assembler.py"

Write-Host ""
Write-Host "F. RC4-7A focused Reference regressions..."
python -m pytest -q `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py"

Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING

Write-Host ""
Write-Host "=============================================================="
Write-Host "RC4-7A Regression Repair R1 completed."
Write-Host "Repository-wide tests were intentionally not run."
Write-Host "Next boundary after PASS: resume RC4-7B argument-flow audit."
Write-Host "=============================================================="
