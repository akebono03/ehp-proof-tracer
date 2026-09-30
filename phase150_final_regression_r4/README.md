# Phase 150 Final Regression R4

This package changes no production code, existing tests, or documentation.

It performs the Phase 150 end-of-phase full regression.

Behavior:
- collect-only preflight
- complete `tests` suite
- short traceback mode (`--tb=line`)
- 50 slowest durations of at least 1 second
- detailed per-test START/END trace from 30% onward
- persistent pytest and trace logs

Completion condition: pytest exit code 0.
