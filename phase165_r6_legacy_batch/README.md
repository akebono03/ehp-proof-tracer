# Phase 165 R6 – Scoped Legacy Repository Test Cleanup

This batch retires only Phase 80–129 tests whose recorded collection errors cite a directly imported missing `repository_*` module. An existing test that imports a candidate blocks its deletion. Every removed test is copied, SHA-256 verified, and recorded for rollback. Production files, current narrative tests, and other tests are not altered. The initial 497-error audit is a historical classification snapshot; counts will not reflect earlier removals.

Run `run.ps1` from the unzipped directory. Results are stored in `phase165_r6_audit_results/legacy_batch/<timestamp>/report.json` with verified original copies in `backup/`. To restore, run `rollback.ps1 -Session '<full session path>'`. This batch does not run full pytest and does not certify Phase 165 closure.
