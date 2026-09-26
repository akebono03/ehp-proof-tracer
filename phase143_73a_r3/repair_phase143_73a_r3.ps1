$ErrorActionPreference = "Stop"

python ".\phase143_73a_r3\repair_phase143_73a_r3.py"

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py"
