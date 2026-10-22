# Phase 168 R2-8(2): Structured Generator Comparison Audit — Collection Fix

This package performs a read-only comparison of nine unresolved citation cases using the existing `HyoujiGen.csv` / `sphere.csv` structured-generator path. It does not change production implementations or certify mathematical identity.

## Run

Extract this package into the repository root, overwriting existing package files. Run from PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase168_r2_8_2_structured_generator_audit\run.ps1"
```

The previous package used the generic test basename `test_audit.py`, colliding with Phase 168 R2-8(1) when both were passed to pytest. This package renames its four tests to `test_phase168_r2_8_2_structured_comparison.py`, removes **only** the obsolete `test_audit.py` inside its own package when the runner starts, and uses pytest `--import-mode=importlib`. The Phase R2-8(1) test file remains untouched. Eight focused tests are selected; the full suite is not executed.

Review `phase168_r2_8_2_structured_generator_audit/output/structured_comparison.json` for typed trees, field-level syntactic differences, raw DB rows, and citation classes. Equality of IDs or printed symbols is not treated as proof of generator identity.
