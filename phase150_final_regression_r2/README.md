# Phase 150 Final Regression R2

This package performs the final Phase 150 full regression after Performance
Repair R1.

It makes no production, test, or documentation changes.

The runner executes:

`python -m pytest tests -q --durations=50 --durations-min=1.0`

The duration report is collected in the same full-suite run so that no second
full regression is needed merely for performance measurement.

Outputs:

- `phase150_final_regression_r2.txt`
- `phase150_final_regression_r2_summary.txt`

If pytest passes, the next step is Phase 150 documentation/closure.
If pytest fails, documentation is not finalized; inspect the failure first.
