Phase 162 R7-B: Delta(iota_5) Provenance Audit

Read-only. No production source or existing tests are modified.
Does not infer proof ownership from textual identity.

Run from the repository root:
  powershell -ExecutionPolicy Bypass -File ".\phase162_r7b_delta_provenance\run.ps1"

Requires previously installed directories:
  phase162_pi5_3_renderer_audit/
  phase162_r7_b_selection_audit/

Produces pi5_3_r7b_delta_provenance.txt and prints it.
Only focused tests are executed; no full suite.
