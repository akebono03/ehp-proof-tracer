$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 150 RC4-7B-2 Intermediate-Conclusion Handoff Audit"
Write-Host "Production changes: none"
Write-Host "=============================================================="

$env:PYTHONPATH = (Get-Location).Path
$env:PYTHONIOENCODING = "utf-8"

Write-Host ""
Write-Host "A. Syntax preflight..."
python -m py_compile `
  ".\phase150_rc4_7b_2_intermediate_conclusion_handoff_audit\audit_phase150_rc4_7b_2.py"

Write-Host ""
Write-Host "B. Running cross-group handoff audit..."
python `
  ".\phase150_rc4_7b_2_intermediate_conclusion_handoff_audit\audit_phase150_rc4_7b_2.py" |
  Tee-Object `
    -FilePath ".\phase150_rc4_7b_2_intermediate_conclusion_handoff_audit\rc4_7b_2_output.txt"

Write-Host ""
Write-Host "C. Focused regression guard..."
python -m pytest -q `
  ".\tests\test_phase143_41_argument_local_body.py" `
  ".\tests\test_phase143_46_multi_argument_narrative_assembler.py" `
  ".\tests\test_phase144_6_r5_43_11_completion_cross_group_narrative_audit.py" `
  ".\tests\test_phase147_rc1_argument_method_ownership.py" `
  ".\tests\test_phase148_rc2_4_repair_r5.py" `
  ".\tests\test_phase148_rc2_4_repair_r5_r2.py" `
  ".\tests\test_phase150_rc4_7a_cross_group_reference_normalization.py"

Remove-Item Env:PYTHONPATH
Remove-Item Env:PYTHONIOENCODING

Write-Host ""
Write-Host "=============================================================="
Write-Host "RC4-7B-2 audit completed."
Write-Host "No production files or existing tests were changed."
Write-Host "Repository-wide tests were intentionally not run."
Write-Host "Next: classify implicit handoff paths before any RC4-7B production change."
Write-Host "=============================================================="
