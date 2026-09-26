$ErrorActionPreference = "Stop"

python ".\phase143_75i\apply_phase143_75i.py"

Copy-Item `
  ".\phase143_75i\test_phase143_75i_whitehead_hopf_semantic_rendering.py" `
  ".\tests\test_phase143_75i_whitehead_hopf_semantic_rendering.py" `
  -Force

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py" `
  ".\tests\test_phase143_75i_whitehead_hopf_semantic_rendering.py"

Write-Host "Phase 143-75I files prepared."
