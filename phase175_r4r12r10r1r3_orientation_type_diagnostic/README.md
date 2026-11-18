# Phase 175 R4R12R10R1R3 — Orientation 1 Typed Mismatch Diagnostic

Read-only inspection of the exact typed mismatch between the existing Toda (5.11) source relation and the second route of the generic EHP quotient provider.

This phase does **not** install, change, or relax a mathematics rule, rewrite a generator, make a new GIVEN, prove Toda (5.11), or complete the target group. It does not modify production files. It examines the exact registered database-derived generators and records dataclass field-level differences rather than guessing an equivalence from notation.

## Requirements

Unzip into the root of `akebono03/ehp-proof-tracer`, branch `develop`, with the R9 Git commit `bf0d7be3081c61f2feec075a3c82c2004c29bbf2` as an ancestor. The prior R10R1 source package must already be present. The R10R1 installer has **not** been run successfully yet, which is acceptable.

## Execution

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r4r12r10r1r3_orientation_type_diagnostic\run.ps1" -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File ".\phase175_r4r12r10r1r3_orientation_type_diagnostic\run.ps1"
```

Both modes run only the four focused tests. Read the `LHS_DIFFERENCES` and `RHS_DIFFERENCES` output lines, and inspect `output/audit_report.json` for full, nested type information. The expected gate is `PASS_R4R12R10R1R3_TYPED_MISMATCH_DIAGNOSED_NOT_COMPLETE`. The gate means only that diagnostic data was captured, **not** that the group was proven.

## Verification boundary

The adopted Toda TeX transcription is pinned by the existing R10R1 source verifier; the original print edition has not been independently verified. The comparison tests type/structure, not semantic equality in the homotopy group. The full pytest suite is reserved for the end of Phase 175.
