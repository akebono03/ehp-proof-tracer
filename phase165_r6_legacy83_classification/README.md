# Phase 165 R6 legacy test classification

Read-only classification of 83 historical test functions in six Phase 49/56 test files.

Run from the EHP Proof Tracer root with `powershell -ExecutionPolicy Bypass -File .\phase165_r6_legacy83_classification\run.ps1`.

This audit does not assert mathematical coverage equivalence or approve test retirement. It does not modify production code or existing tests. It writes `classification.csv` and `summary.json` under `phase165_r6_audit_results/legacy83_classification` and runs three focused tests.
