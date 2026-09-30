$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 149 RC3-3 Minimal Narrative Ordering Implementation"
Write-Host "RC2 exposure unchanged; OWNED_PRIMARY exactness placement only"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying minimal production change..."
python ".\phase149_rc3_3_minimal_implementation\apply_phase149_rc3_3.py"

Write-Host ""
Write-Host "B. Installing focused RC3-3 test..."
Copy-Item `
  ".\phase149_rc3_3_minimal_implementation\test_phase149_rc3_3_minimal_ordering.py" `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
  -Force

Write-Host ""
Write-Host "C. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_argument_body_renderer.py" `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py"

Write-Host ""
Write-Host "D. Running RC3-3 focused tests..."
pytest -q `
  ".\tests\test_phase149_rc3_3_minimal_ordering.py" `
  ".\tests\test_phase148_rc2_4_cross_group_audit.py" `
  ".\tests\test_phase148_rc2_4_post_repair_six_group.py"

Write-Host ""
Write-Host "=============================================================="
Write-Host "RC3-3 focused run completed."
Write-Host "Repository-wide tests are intentionally deferred to RC3-5."
Write-Host "Next: RC3-4 cross-group ordering audit."
Write-Host "=============================================================="
