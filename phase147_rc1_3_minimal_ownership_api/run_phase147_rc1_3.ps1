$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 147 RC1-3 Minimal Argument-Method Ownership API"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying minimal production/test changes..."
python ".\phase147_rc1_3_minimal_ownership_api\apply_phase147_rc1_3.py"

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_exactness_selection.py" `
  ".\toda_group_proof_narrative_argument_multi_renderer.py" `
  ".\tests\test_phase147_rc1_argument_method_ownership.py"

Write-Host ""
Write-Host "C. Phase 147 RC1-3 ownership tests..."
python -m pytest `
  ".\tests\test_phase147_rc1_argument_method_ownership.py" `
  -q

Write-Host ""
Write-Host "D. Focused existing regression..."
python -m pytest `
  ".\tests\test_phase143_19_method_evidence.py" `
  ".\tests\test_phase143_25_relevant_groups.py" `
  ".\tests\test_phase143_28_exactness_selection.py" `
  ".\tests\test_phase143_34_argument_header_method.py" `
  ".\tests\test_phase143_36_argument_body_blocks.py" `
  -q

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 147 RC1-3 focused run complete."
Write-Host "Repository-wide tests are intentionally NOT run in RC1-3."
Write-Host "=============================================================="
