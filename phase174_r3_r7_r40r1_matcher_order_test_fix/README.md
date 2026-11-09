# Phase 174 R3-R7 R40R1 — Inference-Matcher Test Fix

This package corrects exactly one erroneous R40 test assertion. The shared inference matcher binds premise steps by their respective typed patterns, so valid premises may be supplied in reverse order. The corrected test continues to reject a forged generator-zero `GIVEN` and a missing premise.

## Scope

- Changed: `phase174_r3_r7_r40_adopted_db_zero_image_isolated/tests/test_rule.py` (one complete test function).
- Unchanged: R40 mathematics, source guard, adopted DB prior validation, public provider, APIs, rendering, and historical tests.
- The complete original and corrected test files are included under `baseline/` and `replacement/`.
- Source validation verifies the reviewed Git checkout and pinned R40 source files before editing.
- The normal run executes the R40R1 patch tests and the original R40 focused audit. No project-wide pytest is run.

## Windows PowerShell

Extract this ZIP into the repository root. Then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r40r1_matcher_order_test_fix\run.ps1' -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File '.\phase174_r3_r7_r40r1_matcher_order_test_fix\run.ps1'
```

Review `AUDIT_PLAN_JA.md`, `CODE_FULL_JA.md`, and `TEST_RESULTS_JA.md` for details.
