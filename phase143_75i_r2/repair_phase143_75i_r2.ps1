$ErrorActionPreference = "Stop"

Copy-Item `
  ".\phase143_75i_r2\test_phase143_75i_whitehead_hopf_semantic_rendering.py" `
  ".\tests\test_phase143_75i_whitehead_hopf_semantic_rendering.py" `
  -Force

python -m py_compile `
  ".\tests\test_phase143_75i_whitehead_hopf_semantic_rendering.py"

Write-Host "Phase 143-75I R2 test repair applied."
Write-Host "Production code unchanged."
