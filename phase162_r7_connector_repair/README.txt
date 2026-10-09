Phase 162 R7-A: duplicate connector normalization only.
Run from EHP Proof Tracer repository root:
  powershell -ExecutionPolicy Bypass -File .\phase162_r7_connector_repair\run.ps1
Changed: normalize_toda_group_proof_narrative_connectors in toda_group_proof_narrative_contribution_renderer.py.
No imports changed. Existing tests and proof algorithms are untouched.
The full suite is not run. The broader proof-body relevance audit remains R7-B.
