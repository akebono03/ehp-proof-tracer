# Phase 144-6 R25-10 — Final Regression Ownership Audit

## Scope

Audit only. No production code is changed.

The Phase 144-6 completion gate passed the explicit R25-9A/R25-9B checks, then
stopped because the local Phase 144-6 test population had 32 failures.

This audit identifies ownership before any repair.

## Questions

- Which representative groups account for the population increase?
- Which pi_6^3 argument owns the sixth contribution?
- Which detached rows became insertable?
- What provider/anchor information accompanies those rows?
- Does the pi_6^3 transition inventory reflect the same ownership change?
- Where does the numbered connector disappear in the public depth-2 Narrative?
- Is the recursive-repr guard a separate regression?

## Production changes

None.

## Output

The runner writes:

`phase144_6_r25_10_output.txt`

Please preserve or upload that output after the run.

## Tests

Only four representative failing test files are re-run after the audit.
Their failures are expected because R25-10 is audit-only.

The full suite is intentionally not run.

## Completion condition

R25-10 is complete when the diagnostic output identifies a minimal repair
boundary for the final Phase 144-6 regressions.
