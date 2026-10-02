Phase 155 Closure-R3-R1 — runner syntax repair

Cause
-----
The original Closure-R3 planner completed successfully:
- routine tests: 10392
- routine files: 837
- audit-only excluded: 5
- shards: 8

Execution then stopped before shard 1 because the generated runner contained
a Python `try:` block without a matching `except` or `finally`.

Repair
------
- replace only the external shard runner;
- keep the same shard plan;
- do not recollect tests;
- do not modify repository files;
- keep the 600-second per-shard timeout;
- keep checkpoint/resume behavior;
- keep the 5 audit-only nodeids excluded.

The repaired runner writes each pytest shard directly to its shard log and
prints the completed log after the subprocess exits. This avoids the malformed
streaming loop while preserving deterministic timeout handling.

No production/test repository files are changed.
No Phase156 functionality is implemented.
