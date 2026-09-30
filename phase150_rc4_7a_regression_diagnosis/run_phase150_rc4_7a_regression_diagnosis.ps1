$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7A Regression Diagnosis"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "A. Syntax preflight..."
python -m py_compile `
  ".\phase150_rc4_7a_regression_diagnosis\audit_phase150_rc4_7a_regression.py"

Write-Host ""
Write-Host "B. Exactness / Reference replacement diagnosis..."
python `
  ".\phase150_rc4_7a_regression_diagnosis\audit_phase150_rc4_7a_regression.py" |
  Tee-Object `
    -FilePath ".\phase150_rc4_7a_regression_diagnosis\rc4_7a_regression_output.txt"

Write-Host ""
Write-Host "C. Reproducing the four Phase 148 regressions..."
python -m pytest -q `
  ".\tests\test_phase148_rc2_4_repair_r5.py::test_phase148_rc2_4_repair_r5_audit_reproduces_one_visible_raw_exactness" `
  ".\tests\test_phase148_rc2_4_repair_r5_r2.py::test_phase148_rc2_4_repair_r5_r2_remaining_exactness_phrase_is_distinct_from_raw_window"

Write-Host ""
Write-Host "D. Reproducing the independent Phase 143 Reference-placement regression..."
python -m pytest -q `
  ".\tests\test_phase143_46_multi_argument_narrative_assembler.py::test_phase143_46_pi15_8_single_argument_has_no_discourse_marker"

Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING

Write-Host ""
Write-Host "=============================================================="
Write-Host "Diagnosis completed."
Write-Host "No production files were changed."
Write-Host "Repository-wide tests were intentionally not run."
Write-Host "=============================================================="
