# Phase 175 R4R7R1 — Reviewed R4R6 Commit Lineage Fix

This package retains the isolated, typed, conditional inference from Toda Proposition 2.5 introduced in R4R7. It updates the read-only audit to accept the independently reviewed `175-4-6` commit while retaining exact source and provenance guards. No mathematical rule, GIVEN, or production implementation changes in R4R7R1.

## Reviewed Git lineage

- Original review base: `c48fdc307ba67a5e21b0ef49d57953468f7b47e2`.
- Exact reviewed R4R6 successor: `11968d23724cee147520b5fa3fd5a6e89989003e`.
- The successor is verified to descend from the original review base and to add **exactly eight R4R6 audit package files**. Other commits or changes fail closed.
- Pinned Git blob identities for mathematical code and literature remain unchanged.
- The R4R6R2 `audit.py` SHA256 must remain the reviewed value, and the real successful R4R6 report is validated without treating an audit report as a proof.

## Execution

Extract the ZIP at the root of the `akebono03/ehp-proof-tracer` checkout on `develop`. Preserve the completed R4R6 report. Execute `phase175_r4r7_prop25_typed_composition/run.ps1 -DryRun -R4R6Report <report.json>` and then the same command without `-DryRun`. This script runs focused tests only, not the full suite.

Expected final gate: `PASS_R4R7_PROP25_TYPED_INFERENCE_ISOLATED_NOT_PUBLIC`.

## Scope boundary

This update changes only the R4R7 audit history guard, focused audit tests, and package documentation. The existing isolated general rule remains unchanged and disconnected from public Proof Search. The signed formula is not silently rewritten as unsigned; the goal `π_9^5` remains incomplete.
