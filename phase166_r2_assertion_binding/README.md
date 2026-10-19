# Phase 166 R2 — Typed Assertion Candidate Binding

This package performs a **read-only** candidate binding between two display-matching records in `sphere_relation2.csv` and the existing Toda (5.3) assertion component. It uses the existing `AssertionInstantiation` type without modifying the registry or creating a `ProofStep` or `ProofStepLink`. A candidate is **not** certified mathematical equality or permission to cite.

## Prerequisites

Run from the repository root with `phase166_r2_typed53/audit.py`, `sphere_relation2.csv`, and the existing production modules available.

## Windows execution

```powershell
powershell -ExecutionPolicy Bypass -File .\phase166_r2_assertion_binding\run.ps1
```

Outputs are written into `phase166_r2_assertion_binding/results/`. Only targeted tests are executed. Do not treat this as completion of Phase 166 R2 or as completion of the full test suite.
