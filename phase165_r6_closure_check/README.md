# Phase 165 R6 closure check

This package performs a read-only collection audit and a limited focused test run. It does **not** remove tests, update production code, or run the full pytest suite.

Unpack to the repository root and run `powershell -ExecutionPolicy Bypass -File .\phase165_r6_closure_check\run.ps1`.

Results: `phase165_r6_audit_results/closure_check/report.json`, `collection.stdout.txt`, and `focused.stdout.txt`. Review the full collection log before removing any tests; a collection error alone does not prove a test is obsolete. The current method checks root-level `test_phase165*.py` candidates for focused execution; this is not full current-path coverage certification.
