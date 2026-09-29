# Phase 144-6 Final Regression Repair R23

## Production changes
None.

## Test change
- `tests/test_phase143_61b_r_semantic_suppression_priority.py`
- `test_phase143_61b_r_keeps_pi6_3_local_connector`

The old Phase143 assertion required the literal generic connector
`これらより、` in final output. Phase144-5-R2 intentionally transforms that
connector into actual equation references such as `(1) と (2) より、`.

R23 updates only the stale assertion to the current Phase144-5 contract.

## Regression
Runs the directly related Phase143-57c, Phase143-61b, Phase143-61b-R and
Phase144-5 tests.

No full suite is run.
