# Phase 144-6 Final Regression Repair R9

## Scope

This repair changes only:

- `tests/test_phase143_15_argument_ordering.py`

Production code is not changed.

## Diagnosis

The current `pi_16^9` NarrativeArgument population has three arguments:

1. group structure for `pi_16^9`, with child index 1,
2. definition of `sigma_9`,
3. detached definition of `sigma'''`.

The current production ordering is therefore `(2, 1, 0)`.

The old Phase 143 test expected the exact source-index tuple `(1, 0)`. That
expectation encoded the historical two-argument population rather than the
semantic invariant named by the test.

## Repair

The `pi_16^9` test now verifies the intended semantic invariant directly:

- locate the definition argument whose purpose subject is `sigma_9`;
- locate the group-structure argument;
- require the `sigma_9` definition to precede the group structure.

The detached `sigma'''` definition is not constrained by this Phase 143 test.
Its presence and ordering are handled by the newer generic Narrative machinery.

Other Phase 143-15 ordering tests retain their existing exact-order contracts.

## Run

From the repository root:

```powershell
powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_final_regression_repair_r9\run_phase144_6_final_regression_repair_r9.ps1"
```

The runner performs focused tests only. It intentionally does not run the full
suite.
