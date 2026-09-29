$ErrorActionPreference = "Stop"

Write-Host "=============================================================="
Write-Host "Phase 147 RC1-3 Repair R1"
Write-Host "=============================================================="

Write-Host ""
Write-Host "A. Applying the three minimal repairs..."
python ".\phase147_rc1_3_repair_r1\apply_phase147_rc1_3_repair_r1.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "B. Syntax preflight..."
python -m py_compile `
  ".\toda_group_proof_narrative_exactness_selection.py" `
  ".\toda_group_proof_narrative_argument_multi_renderer.py" `
  ".\tests\test_phase147_rc1_argument_method_ownership.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "C. Phase 147 RC1-3 ownership tests..."
python -m pytest `
  ".\tests\test_phase147_rc1_argument_method_ownership.py" `
  -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "D. Focused existing regression..."
python -m pytest `
  ".\tests\test_phase143_19_method_evidence.py" `
  ".\tests\test_phase143_25_relevant_groups.py" `
  ".\tests\test_phase143_28_exactness_selection.py" `
  ".\tests\test_phase143_34_argument_header_method.py" `
  ".\tests\test_phase143_36_argument_body_blocks.py" `
  -q
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host ""
Write-Host "=============================================================="
Write-Host "Phase 147 RC1-3 Repair R1 focused tests: PASS"
Write-Host "Repository-wide tests intentionally not run."
Write-Host "=============================================================="
