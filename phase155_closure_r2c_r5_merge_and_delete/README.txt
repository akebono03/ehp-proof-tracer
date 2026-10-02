Phase 155 Closure-R2C-R5 — merge five candidates and delete six redundant tests

Merge result
------------
Five MERGE_CANDIDATE tests become two audit-only tests:

1. Phase153 all-group Reference population audit
   - selected statement exists;
   - [R#] marker exists;
   - selected statement is publicly visible;
   - one 112-group traversal instead of three.

2. Phase97 representative cross-layer provenance audit
   - source candidate goal_source identity;
   - presentation goal-source identity;
   - repository-source identity;
   - phase / theorem / branch_name;
   - six representative targets in one top-level integration audit.

Delete result
-------------
Six DELETE_CANDIDATE functions are removed after R2C-R4 proved that their
contracts are covered by later/current lightweight or public-surface tests.

Both merged tests are opt-in audit-only tests. R2C-R5 does not execute them.

No production code changes.
No repository-wide pytest.
