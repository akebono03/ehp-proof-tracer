$ErrorActionPreference = "Stop"

python ".\phase143_73a_r5\repair_phase143_73a_r5.py"

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py"
