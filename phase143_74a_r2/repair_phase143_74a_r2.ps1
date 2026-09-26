$ErrorActionPreference = "Stop"

Copy-Item `
  ".\phase143_74a_r2\test_phase143_74a_map_narrative.py" `
  ".\tests\test_phase143_74a_map_narrative.py" `
  -Force

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase143_74a_map_narrative.py"

Write-Host "Phase 143-74A R2 test repair applied."
Write-Host "Implementation file was not changed."
