Phase 163 R4-R7: representative ProofStep bindings (opt-in, fail-closed)

Extract ZIP into the repository root and execute:
  powershell -ExecutionPolicy Bypass -File .\phase163_r4_r7_representative_bindings\run.ps1

The script installs only the two named new Python files, runs focused R6/R7
pytest, then attempts actual representative bindings with existing Phase 58 and
Phase 65 proof witnesses. Verification failures stay metadata-only and are
reported. No source rule, proof search, renderer or entire registry is modified.
Outputs: phase163_r4_r7_output/report.md and summary.json
