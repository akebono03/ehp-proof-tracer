# Phase 165 R14-R1: Typed Goal Frontier

This package uses the current project classes to construct the genuine typed target `pi_3^2 = Z{eta_2}` and interrogate the registered Toda source archive. This is a read-only diagnostic, not a proof. It never calls legacy proof replay, never manufactures a `ProofStep`, and never promotes an unverified Toda citation.

## Changed or added units

- New `phase165_r14_goal_frontier.py`: `TypedGoalFrontier`, `build_free_cyclic_group_goal`, `inspect_free_cyclic_goal`.
- New `audit.py`: writes `phase165_r14_output/report.json` and `.md`.
- New focused tests `test_phase165_r14_goal_frontier.py`.
- New `run.ps1`: targeted tests only, followed by audit.

All new modules are in the package directory. Production files and preexisting public APIs are untouched. `PYTHONPATH` points to the package and project root for the runner.

## Success criterion

The report contains the correct typed mathematical goal; all 117 source assertions remain non-promoted; missing proof dependencies produce an explicit `UNRESOLVED` status rather than an old narrative. The next increment must introduce source-verified, general typed premises and a non-specialized rule expansion provider before claiming mathematical proof. Whole-suite tests remain deferred until Phase 165 closure.
