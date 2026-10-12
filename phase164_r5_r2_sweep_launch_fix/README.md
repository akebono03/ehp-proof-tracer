# Phase 164 R5-R2 — Sweep launch correction

This package fixes only the way the existing 112-target sweep is launched.
The previous runner executed a script inside a subdirectory by pathname,
which excluded the project root from Python's module search path. Running
it with `python -B -m phase164_r5_r2_unified_web_display.sweep_112` from the
repository root fixes the import without changing production Python code.

The original targeted tests already passed (14 passed). This runner repeats
only the 112-target sweep. It does not run the full pytest suite, apply the
original patch again, or modify proof/rendering code.

Unzip in the repository root and run
`powershell -ExecutionPolicy Bypass -File .\phase164_r5_r2_sweep_launch_fix\run.ps1`.
Review `phase164_r5_r2_output/report.json` for the actual 112-target result.
