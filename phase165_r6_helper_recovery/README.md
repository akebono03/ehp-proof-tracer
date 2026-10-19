# Phase 165 R6: historical test helper recovery

This package does not modify production code or restore retired inference rules, repositories, or renderers. It searches the local Git history and existing local R6 backup folders for the *actual historical file* `tests/test_phase143_19_method_evidence.py`. It never synthesizes a replacement implementation.

The file is restored only if its syntax and dependencies pass static checks and two targeted tests execute successfully. If either targeted test fails, the candidate file is removed again. When no acceptable source exists, the workspace is unchanged. Logs and a report are written beneath `phase165_r6_audit_results/helper_recovery/`.

The remaining 142 legacy-probe-related collection errors are deliberately untouched; they involve transitive dependencies that require careful modernization. No full suite is run here.

To revert a successful recovery, remove only `tests/test_phase143_19_method_evidence.py` after confirming the `RESTORED_TARGETED_TESTS_PASS` report. It was absent at the beginning of this run.
