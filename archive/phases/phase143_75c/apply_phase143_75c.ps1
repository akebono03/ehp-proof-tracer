$ErrorActionPreference = "Stop"

python ".\phase143_75c\apply_phase143_75c.py"

Copy-Item `
  ".\phase143_75c\test_phase143_75c_generic_semantic_rendering.py" `
  ".\tests\test_phase143_75c_generic_semantic_rendering.py" `
  -Force

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase143_75c_generic_semantic_rendering.py"

Write-Host "Phase 143-75C files prepared."
