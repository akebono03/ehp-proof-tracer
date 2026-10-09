Phase 162 R3-I: Existing Semantic Sidecar alignment inventory

No production code changes. Read-only audit of the 54 unexplained inferences
from Phase 162 R3-H against existing semantic, aggregate, and reason sidecars.

Run from the ehp-proof-tracer repository root in PowerShell:
  Expand-Archive -Path "$HOME\Downloads\phase162_r3i_semantic_sidecar_audit.zip" -DestinationPath . -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r3i_semantic_sidecar_audit\run_phase162_r3i.ps1"

Outputs (phase162_r3i_output):
- semantic_sidecar_audit.json
- semantic_sidecar_entries.json
- semantic_sidecar_groups.json

The audit does not certify a proof or attach candidates to the recursive
Renderer. Final-result labels remain unverified; direct/contextual semantic
reasons remain candidates until mathematical sufficiency is audited.
Focused tests only. Full suite is not run.
