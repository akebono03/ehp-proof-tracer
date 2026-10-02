Phase 155-R6 — pytest collection / runtime audit

This R6 package may be moderately heavy.

What it does
------------
1. Runs pytest collection in checkpointed file batches.
2. Maps collected pytest cases back to the R5 execution lanes.
3. Runs only a small deterministic runtime probe from each lane.
4. Records slow/timeout candidates for Phase 155 closure planning.

What it does NOT do
-------------------
- It does not run the 9,069-test canonical regression.
- It does not run repository-wide pytest.
- It does not delete or modify tests.
- It does not modify production code.

Progress / resume
-----------------
Collection prints:

  [collect N/M] START ...
  [collect N/M] PASS ...

Each successful batch is checkpointed.

On rerun:

  [collect N/M] checkpoint PASS - skip

Runtime probes are checkpointed one by one in the same way.

Runtime scope
-------------
The deterministic probe is intentionally small:

- canonical_routine: 3 source test functions
- historical_compatibility: 2
- audit_only: 2
- performance_heavy_integration: 3
- residual_retained: 2

Maximum: 12 runtime probes.

Each probe has a 60-second timeout.

This is a measurement sample, not a full regression and not a statistically
precise total-runtime estimate.

Future test policy
------------------
- New tests are lightweight by default.
- all-group / cross-group / population scans do not enter the routine canonical
  lane.
- heavy integration tests are explicitly separated at creation.
- long-running audit tools show progress and support checkpoint/resume.
