Phase 162 R2 — Validated Proof Presentation Adapter

Changed/new files:
- NEW phase162_validated_proof_presentation.py
  - ValidatedProofPresentation
  - _ordered_premises
  - build_validated_backward_proof_presentation
  - render_validated_backward_proof_markdown
- NEW tests/test_phase162_r2_validated_proof_presentation.py

This deliberately does NOT change TodaGroupResult / TodaGroupProofPresentation,
the existing public group narrative API, references, or web entry points.
R2 uses the existing common _render_generic_narrative_step on the actual R7
validated ProofStep ancestry. It does not claim that the group-level public
renderer accepts map-goal presentations yet. Reference ownership remains R3.

Run (PowerShell, from repository root):
  Expand-Archive -Path "$HOME\Downloads\phase162_r2_validated_presentation_adapter.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r2_validated_presentation_adapter\run_phase162_r2.ps1"

To view output after focused tests:
  python -c "from tests.test_phase162_r2_validated_proof_presentation import _validated_fixture; from phase162_validated_proof_presentation import build_validated_backward_proof_presentation,render_validated_backward_proof_markdown; print(render_validated_backward_proof_markdown(build_validated_backward_proof_presentation(_validated_fixture())))"

Scope: R2 only. No full test suite. No repository modification on GitHub.
