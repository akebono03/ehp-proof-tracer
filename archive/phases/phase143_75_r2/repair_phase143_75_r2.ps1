$ErrorActionPreference = "Stop"

Copy-Item `
  ".\phase143_75_r2\audit_phase143_75_machine_like_narrative.py" `
  ".\phase143_75\audit_phase143_75_machine_like_narrative.py" `
  -Force

python -m py_compile `
  ".\phase143_75\audit_phase143_75_machine_like_narrative.py"

Write-Host "Phase 143-75 R2 audit repair applied."
Write-Host "Production implementation was not changed."
