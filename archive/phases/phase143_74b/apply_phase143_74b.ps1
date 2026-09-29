$ErrorActionPreference = "Stop"

python ".\phase143_74b\apply_phase143_74b.py"

Copy-Item `
  ".\phase143_74b\tests\test_phase143_74b_remaining_internal_narrative.py" `
  ".\tests\test_phase143_74b_remaining_internal_narrative.py" `
  -Force

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase143_74b_remaining_internal_narrative.py"

Write-Host "Phase 143-74B files prepared."
