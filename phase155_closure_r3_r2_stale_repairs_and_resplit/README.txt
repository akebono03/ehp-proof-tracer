Phase 155 Closure-R3-R2
- preserve PASS shards 1,2,6,7
- repair stale Phase144/153/96 tests
- split original shard 3 into 3 jobs
- split original shard 4 into 3 jobs
- rerun original shard 5 as 1 job
- rerun original shard 8 as 1 job
- exclude audit-only tests
- no production changes
- no monolithic pytest
