Phase 162 R3-B: run the existing, unmodified Narrative Renderer against the
Phase 162 R2 conclusion-driven proof tree validated in R3-A.

Run from repository root in PowerShell:
  Expand-Archive -Path "$HOME\Downloads\phase162_r3b_existing_renderer_audit.zip" -DestinationPath . -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r3b_existing_renderer_audit\run_phase162_r3b_existing_renderer.ps1"

Adds only audit_phase162_r3b_existing_renderer.py and its focused test.
Requires R3-A Repair2 already installed (audit_phase162_r3a_presentation.py).
Does not alter R2, Phase 161, existing Renderer, or production routes.

Output at repository root:
  phase162_r3b_output/r2_production_narrative_raw.md
  phase162_r3b_output/renderer_audit.json
  phase162_r3b_output/step_diagnostics.json

NOTE: The raw Markdown is the exact public production Renderer return value.
Diagnostic counts are conservative: they do not prove mathematical reasoning
coverage, and a missing exact snippet is not necessarily a rendering defect.
Entire test suite is NOT run.
