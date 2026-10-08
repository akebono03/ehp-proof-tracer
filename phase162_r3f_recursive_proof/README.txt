Phase 162 R3-F: Recursive ProofStep trace (NOT a finished proof)

Requires Phase 162 R3-E and R3-B already applied in the repository root.
From repository root run:
  powershell -ExecutionPolicy Bypass -File ".\phase162_r3f_recursive_proof\run_phase162_r3f.ps1"

Files added to repository root:
  phase162_r3f_recursive_renderer.py
  audit_phase162_r3f.py
  tests/test_phase162_r3f_recursive_renderer.py

Output directory: phase162_r3f_output/
  recursive_proofstep_trace.md  All nodes in dependency-first order
  recursive_trace_audit.json  Honest counts of explained/unexplained steps
  recursive_step_index.json  Per-node dependency indices and reason statuses

The only explained INFERENCE is the verified root transport. All other
INFERENCE steps are marked UNEXPLAINED. Public renderer remains unchanged.
Full test suite intentionally not run.
