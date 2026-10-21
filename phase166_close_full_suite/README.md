# Phase 166 Closure — Full Pytest

This package runs the full repository pytest suite once at the end of Phase 166. It does not modify project production code, existing tests, or project documentation. It captures the complete test output and Git status before and after the run.

Extract the archive into the repository root, then run `powershell -ExecutionPolicy Bypass -File ".\phase166_close_full_suite\run.ps1"`.

Results are stored in `phase166_close_full_suite/results/<UTC timestamp>/`: `pytest_full.log`, `git_before.txt`, `git_after.txt`, and `summary.json`.

A nonzero test exit code blocks closure. A zero test exit code is a closure candidate and should be reviewed before recording official completion. Phase 167 begins only after the Phase 166 close decision.
