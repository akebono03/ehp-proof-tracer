# Phase 163 R4-R66 — One Reference, Multiple Assertions

This read-only audit consumes the R4-R65 `review_packets.json` from the repository root and produces provisional editorial decisions for the 16 definition candidates and 21 proposed assertions. One literature Reference may contain multiple ordered Assertions. It does not verify the original printed edition, approve mathematical semantics, modify the production registry, allocate permanent IDs, or connect proofs.

Run from the repository root (PowerShell):

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r66_multi_assertion_boundary\run.ps1"
```

The runner executes only six focused tests and then writes `phase163_r4_r66_output/boundary_decisions.json` and `boundary_decisions.md`. The full test suite is deferred until the end of Phase 163.

## Changes

Only the new `phase163_r4_r66_multi_assertion_boundary` folder is added. There are no edits to existing repository files, classes, imports, or functions. The new `build_review`, `write_reports`, and `main` functions are contained in `phase163_r4_r66_multi_assertion_boundary.py` and can be reviewed in full.

## Exit criterion and next boundary

A successful run has 16 Reference proposals, 21 Assertion proposals, five multi-Assertion References, zero permanent IDs, and zero mathematically verified boundaries. R4-R67 may validate or expand incomplete source spans and inspect contextual dependencies. It must not infer mathematical verification from an editorial decision alone.
