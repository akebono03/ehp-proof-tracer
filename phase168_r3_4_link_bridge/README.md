# Phase 168 R3-4: Proof-step / citation bridge

This package adds one read-only adapter that projects actual ProofSteps and explicit ProofStepLinks to the R3-3 intermediate model. It does not change the production search or Web renderer.

`run.ps1` copies a complete Python module and one focused test file into the repository, runs the R3-3 and R3-4 targeted pytest files, and produces a diagnostic projection for pi_4^2. The diagnostic does not assert that the production citation metadata is already complete; missing references must be reported, not invented.

Run from the repository root after installing R3-3. No full pytest suite is run.


## R3-4 run script correction
The R3-3 test remains inside `phase168_r3_3_narrative_model/tests` rather than the repository-level `tests` directory. The runner now resolves both test paths explicitly. No production implementation was changed in this correction.

## R3-4 import-path correction
The diagnostic probe is launched from a subdirectory. The runner now adds the repository root to `PYTHONPATH` only while the probe runs and restores the previous environment afterward. The adapter and tests are unchanged.
