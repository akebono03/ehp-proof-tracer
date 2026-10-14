# Phase 165 R57-R1 runner fix

This ZIP replaces only `phase165_r57_r1_single_entry/run.ps1`.

The R57-R1 patch and route inventory had already executed; pytest stopped because the runner expected an R56-R2 test in the repository root, while the test resides in its extracted Phase package.

The corrected script resolves each targeted test from the project root, the current R57 package, or the corresponding extracted Phase package. Missing tests remain fatal. Mathematical implementation, renderer code, proof search, and the AST route audit are unchanged.

Run the repaired R57-R1 `run.ps1` from the repository root after extracting with `Expand-Archive -Force`. It runs only four targeted test modules; full pytest is not run.
