Phase 146 Final Regression Expectation Repair R3

Production changes: none.

R3 discards the R1/R2 whole-file newline churn by restoring the five affected
tests from local Git HEAD, then applies only the Phase 146-7 expectation changes
with byte-level replacements.

No Phase 147 functionality is implemented.

Completion:
- syntax preflight passes
- 31 focused tests pass
- git diff --check passes
- diff contains only small expectation changes

Then run:
  python -m pytest tests -q --durations=50
