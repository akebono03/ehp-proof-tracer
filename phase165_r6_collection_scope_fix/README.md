# Phase 165 R6 scoped collection runner

This package changes only R6 execution tooling. Production and test code are unchanged.

Run the PowerShell script from the repository root. The collector searches `tests/` and top-level `test_*.py` files only. Historical phase directories, archive trees and saved payloads are not recursively collected. This is a **candidate current suite**, not a claim that every selected test is maintained or that excluded historical tests are irrelevant.

Collection errors are saved in `phase165_r6_audit_results/collection.log` and `collection_scope.json`. Any collection error blocks the phase closing gate; it is never classified as a test PASS. If collection succeeds, tests execute in batches of 25 with restart checkpoints. R3 and R4 are executed first; baseline snapshots are never rewritten.

An existing version-1 checkpoint is deliberately refused (it was collected from an incompatible all-directory scope). The old checkpoint is retained for investigation. To start a new inventory, archive the old `resume_state.json` and `collected_nodeids.json`, never overwrite them silently. Logs are appended when running batches.

`Ctrl+C` interrupts a batch; the batch is retried upon restart. Phase closure additionally requires manual Web verification.
