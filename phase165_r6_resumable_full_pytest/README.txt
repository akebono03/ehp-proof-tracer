Phase 165 R6 resumable final regression runner

Changed files:
- phase165_r6_closure_audit/run.ps1 (full replacement; installer backs up old file)
- phase165_r6_closure_audit/resumable_full_pytest.py (new file)

Run install.ps1 first. It does not execute the full pytest suite.
Full-suite runner collects tests and runs groups of 40 nodeids sequentially.
Each completed batch is journaled in phase165_r6_audit_results/resumable_full/state.json.
On Ctrl+C, the running batch is interrupted; the next run repeats only that batch.
Failed batches stop execution and are retried on the next invocation.
The collection set is saved and reused; to make a new test scope after code changes,
archive or remove resumable_full/nodeids.json and state.json together.
Each batch runs in a separate Python process, which may change behavior of tests
that share process-level global state; a full single-process suite is not identical.
Source code, tests, and mathematical proof records are not changed.
