# Phase 165 R6 — Historical Helper Failure Diagnosis

Read-only diagnostic package for the failed recovery of `tests/test_phase143_19_method_evidence.py`.

Run `run.ps1` from the repository root. It finds the latest `phase165_r6_audit_results/helper_recovery/*/report.json` and the adjacent `targeted_pytest.log`, then reports module/export errors, failed tests, and relevant tracebacks. It creates only an output report under `phase165_r6_audit_results/helper_failure_diagnosis/`.

No production files, existing tests, deleted files, or helper candidates are changed. The package runs three self-tests, not the project's full pytest suite. An absent historical traceback remains unknown rather than guessed.
