# Phase 173 R4-R13R1 — Committed HEAD Lineage Guard Fix

This repair only updates `source_guard()` in the uncommitted, read-only
R4-R13 narrative audit package. The old reviewed HEAD was `a9b4617fbef603e4ced2252b7812d2dfa19fc606`;
its legitimate R4-R12 commit is `33f73f1dfb853875589b8fb70bda9853c75a8dae`.

The old R4-R12 installer checks the Web adapter's *pre-commit* Git blob, so
changing the HEAD constant alone would not work. The corrected guard supports
the two precisely reviewed states. The committed state reconstructs the Web
adapter from the reviewed parent, compares exact local and committed bytes,
checks the projector hash, verifies the R4-R11 zero-group proof-route patch,
and rejects any tracked changes, staging, or remote mismatch.

No mathematical rule, proof step, Web renderer, project document or existing
application source file is modified. The new replacement is source-pinned, and
only one complete function in the R4-R13 audit is replaced. The full R4-R13
audit and its focused tests are run after installation.

Extract at the repository root, run `run.ps1 -DryRun`, then `run.ps1`.
The full project test suite remains reserved for the Phase 173 closeout.
