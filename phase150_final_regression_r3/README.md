# Phase 150 Final Regression R3

This package performs the final full regression for Phase 150 after
Performance Repair R1 and R2.

It makes no production, test, or documentation changes.

## Command

The runner executes exactly one full suite:

```text
python -m pytest tests -q --durations=50 --durations-min=1.0
```

The duration report is collected in the same run so that no separate
performance baseline run is required.

## Outputs

- `phase150_final_regression_r3.txt`
- `phase150_final_regression_r3_summary.txt`

## Completion rule

If pytest exits with code 0, Phase 150 correctness regression is complete.
Do not run the full suite again; proceed to Phase 150 documentation/closure.

If pytest fails, do not finalize Phase 150 and do not immediately repeat the
full suite. Diagnose only the reported failures with focused tests.
