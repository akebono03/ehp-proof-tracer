$ErrorActionPreference = "Stop"

python ".\phase143_75f\apply_phase143_75f.py"

Copy-Item `
  ".\phase143_75f\test_phase143_75f_ehp_semantic_rendering.py" `
  ".\tests\test_phase143_75f_ehp_semantic_rendering.py" `
  -Force

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase143_75f_ehp_semantic_rendering.py"

Write-Host "Phase 143-75F files prepared."
