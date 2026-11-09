# Phase 174 R3-R7-R40: Verified Adopted-DB Cyclic Zero Image (Isolated)

This package introduces an **isolated**, generic inference for the zero image of a suspension map. It explicitly distinguishes a verified *adopted earlier database prior* from an independent cited mathematical theorem.

The three conditions are: (1) an actual earlier DB group presentation of the form `Z/m{g}`, accepted and freshly reverified by the existing adoption gate; (2) a separately inferred proof of `E(g) = 0`; and (3) a well-typed suspension map. The conclusion `im(E) = 0` is an `INFERENCE` step with the original adopted `GIVEN` step retained in its ancestry.

**This is not a new source assertion.** No production provider, proof search, renderer, database row, or project-wide documentation is modified. The existing R6 rule still requires two `INFERENCE` premises. R40 adds an alternative specifically for a verified adopted DB prior. The final target and upper Delta surjectivity are not claimed complete.

## Run

Extract into the repository root, then use:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r40_adopted_db_zero_image_isolated\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r40_adopted_db_zero_image_isolated\run.ps1
```

DryRun checks the reviewed repository state without modifying files. A normal run rebuilds real source-backed R39 inference steps, verifies the adopted DB prior, checks the new isolated inference, and runs only focused pytest groups.

Read `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, `IMPORTS_FULL.txt`, and `TEST_RESULTS_JA.md` for the complete design, source, imports and regression plan.
