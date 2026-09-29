Phase 144-6-R5-17A audit package

Purpose:
  Audit pi_6^3 Narrative Arguments by reverse-traversing proof edges from each
  unique Argument conclusion step, without a fixed evidence-depth cutoff.

Production code changes:
  None.

Files copied into the repository:
  audit_phase144_6_r5_17a.py
  tests/test_phase144_6_r5_17a_proof_chain_selection_audit.py

Run from repository root after extracting the ZIP there:

  powershell -ExecutionPolicy Bypass `
    -File ".\phase144_6_r5_17a_audit_package\run_phase144_6_r5_17a.ps1"

Only the Phase 144-6-R5-17A targeted test file is executed.
The full pytest suite is intentionally not run in this subphase.
