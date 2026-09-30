$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 149 RC3-3 Repair R1"
Write-Host "Precollect OWNED_PRIMARY exactness before conclusion placement"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying RC3-3 Repair R1..."
python ".\phase149_rc3_3_repair_r1\apply_phase149_rc3_3_repair_r1.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_argument_body_renderer.py" `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py"

Write-Host ""
Write-Host "C. Re-running RC3-3 + RC2 focused regression..."
pytest -q `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
  ".\tests\test_phase148_rc2_4_cross_group_audit.py" `
  ".\tests\test_phase148_rc2_4_post_repair_six_group.py"

Write-Host ""
Write-Host "=============================================================="
Write-Host "RC3-3 Repair R1 focused run completed."
Write-Host "Repository-wide tests remain deferred to RC3-5."
Write-Host "If all focused tests pass, RC3-3 is complete."
Write-Host "=============================================================="
