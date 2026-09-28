# Phase 144-6 Final Regression Repair R5

## Scope

This repair changes only:

- `tests/test_phase143_15_argument_ordering.py`

Production code is not changed.

## Reason

The Phase 143 ordering test used `id(argument)` to recover the original source
index after ordering. During the Phase 144-6 final full-suite run, the
`pi_16^9` test entered pytest's recursive dataclass representation path while
reporting a lookup failure.

The ordering contract itself remains unchanged. The helper now identifies an
argument by the identity of its `conclusion_block`, which is the semantic
anchor used by the ordering test and avoids making the wrapper Argument
object's identity part of the test contract.

Expected orders remain:

- pi_6^3: `(2, 1, 0)`
- pi_8^5: `(2, 1, 0, 3)`
- pi_16^9: `(1, 0)`

## Run

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_final_regression_repair_r5\run_phase144_6_final_regression_repair_r5.ps1"
```

The runner performs focused tests only. It does not run the full suite.
