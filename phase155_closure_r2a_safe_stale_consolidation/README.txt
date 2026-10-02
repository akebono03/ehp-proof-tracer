Phase 155 Closure-R2A — SAFE_STALE 38 stale expectation consolidation

Scope
-----
Exactly 38 SAFE_STALE failures from Phase132/133/143/150.

No production files are changed.
No imports are changed.
Phase144 HISTORICAL_HEAVY tests are not changed.
Phase153 / Phase95-98 CONTRACT_SENSITIVE tests are not changed.

Repair principle
----------------
Old presentation snapshots are replaced by current semantic invariants.
Mathematical target/result checks and internal-rule-name suppression remain.

Focused verification
--------------------
38 nodeids are split into four checkpointed batches:
1. Phase132/133
2. Phase143 argument renderers
3. Phase143 semantic renderers
4. Phase150

PASS batches are skipped on rerun.
Repository-wide pytest is NOT run.
