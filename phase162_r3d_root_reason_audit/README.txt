Phase 162 R3-D: root inference provenance and public narrative placement audit

Prerequisites: R3-A Repair 2, R3-B, R3-C Repair 1 must already be applied.
This package adds only audit code and a focused test. Existing inference rules,
prose renderers, ProofSteps and project documents are not modified.

From repository root:
  Expand-Archive -Path "$HOME\Downloads\phase162_r3d_root_reason_audit.zip" -DestinationPath "." -Force
  powershell -ExecutionPolicy Bypass -File ".\phase162_r3d_root_reason_audit\run_phase162_r3d.ps1"

Focused tests: tests/test_phase162_r3d_root_reason_audit.py (5 tests).
Output: phase162_r3d_output/root_reason_audit.json and r2_public_narrative_raw.md.
Only the root inference shape, three identity-preserved premise edges,
reason presence and final position are certified. Full prose semantic
certification and 67-inference coverage are deliberately out of scope.
