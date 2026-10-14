# Phase 165 R56-R1 runner repair

The original R56-R1 ZIP stores `test_phase165_r56_r1_generator_suspension_fix.py` inside the extracted package directory, but its runner mistakenly invokes pytest using the project-root relative filename. This causes a collection error even after the renderer fix is installed.

This repair replaces **only** the original R56-R1 `run.ps1`. It preserves the existing `install.py`, all mathematical code, the original focused tests, and the R55/R56 regressions. The runner now resolves its own directory and project root, invokes the already-installed patch idempotently, checks that the three required targeted tests exist, and passes their full paths to pytest. It does not run the full suite.

From the repository root, expand this ZIP with `Expand-Archive -Force`, then run `phase165_r56_r1_generator_suspension_fix/run.ps1`. The two original R56-R1 focused tests and the existing R56 and R55 regressions will execute. Missing tests stop the runner explicitly rather than silently skipping checks.
