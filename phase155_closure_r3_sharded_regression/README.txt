Phase 155 Closure-R3 — final sharded regression

Design
------
- 8 routine shards.
- Audit-only tests are excluded by the Phase155 audit manifest.
- Test files stay contiguous in filename order to preserve phase-local cache reuse.
- Historical slow rows from the previous full-suite log are used only as planning weights.
- The three 508s/281s/276s nodeids are explicitly ignored as historical weights because
  R2C-R2 replaced those test bodies with lightweight contracts.
- Hard timeout: 600 seconds per shard.
- PASS shards are recorded in `phase155_closure_r3_output/checkpoint.json`.
- Rerunning the same PowerShell script skips already-PASS shards.
- No monolithic repository-wide pytest is used.

Outputs
-------
phase155_closure_r3_output/
  routine_collection.json
  shard_plan.json
  checkpoint.json
  shard_01.log ... shard_08.log
  summary.txt

Failure workflow
----------------
If one or more shards fail:
1. do not delete `phase155_closure_r3_output/checkpoint.json`;
2. repair only the failing contract;
3. run the same PowerShell script again;
4. already-PASS shards are skipped.

Phase boundary
--------------
This package only closes Phase155 routine regression.
It does not implement Phase156 Reference-statement relevance/minimal display.
