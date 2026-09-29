$ErrorActionPreference = "Stop"

python ".\phase143_73a_r4\repair_phase143_73a_r4.py"

python -m py_compile `
  ".\toda_group_proof_narrative_renderer.py"

python -m py_compile `
  ".\tests\test_phase143_73a_internal_statement_narrative.py"
