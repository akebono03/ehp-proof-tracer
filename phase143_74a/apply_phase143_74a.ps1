$ErrorActionPreference = "Stop"

python ".\phase143_74a\apply_phase143_74a.py"

Copy-Item `
  ".\phase143_74a\tests\test_phase143_74a_map_narrative.py" `
  ".\tests\test_phase143_74a_map_narrative.py" `
  -Force

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase143_74a_map_narrative.py"

Write-Host "Phase 143-74A files prepared."
