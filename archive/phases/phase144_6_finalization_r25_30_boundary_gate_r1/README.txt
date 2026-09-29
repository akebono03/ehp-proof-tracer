Phase 144-6 Finalization R25-30 Boundary Gate R1

R1 fixes only the runner import path.

Changed file
------------
phase144_6_finalization_r25_30_boundary_gate_r1/
  run_phase144_6_finalization_r25_30_boundary_gate_r1.ps1

Change
------
PYTHONPATH now contains both:
- repository root
- repository root/tests

This is required because audit_phase144_6_r5_43_11d.py imports
test_phase144_6_r5_18_production_generic_proof_chain_foundation as a top-level
module.

No production code is changed.
No existing tests are changed.
No documentation is changed.
No Phase 145 functionality is implemented.
No repository-wide pytest is run.
