# Phase 166 R3-AU — `gen_coe` Cross Audit

This package performs a read-only cross-audit of every row in the sphere database, including stems outside the 112 public groups.

It inventories `gen_coe` encodings as empty values, single basis vectors, basis vectors with coefficients, linear combinations, or invalid encodings. It deliberately does **not** claim a LaTeX match where the current production code has no `gen_coe -> typed expression` conversion path.

Run from the repository root after extracting the ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase166_r3au_gen_coe_cross_audit\run.ps1"
```

Outputs are written to `phase166_r3au_gen_coe_cross_audit/results/`.

This package does not modify production code and does not run the full pytest suite.
