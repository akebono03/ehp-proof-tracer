# Phase 144-6 Final Regression Diagnosis R6

This package performs a compact diagnostic of the `pi_16^9` NarrativeArgument
ordering without using pytest assertion rewriting.

It changes no production code and no persistent tests.

The diagnostic prints only:

- source argument count,
- each argument's role,
- conclusion block role,
- child indices,
- ordered source indices by Argument identity,
- ordered source indices by conclusion-block identity.

This avoids recursively rendering the large proof dataclass graph.

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass `
  -File ".\phase144_6_final_regression_diagnosis_r6\run_phase144_6_final_regression_diagnosis_r6.ps1"
```
