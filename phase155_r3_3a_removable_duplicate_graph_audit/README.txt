Phase 155-R3-3A — removable duplicate graph and canonical survivor audit

Purpose
-------
Convert the 164 R3-2F-r1 `removable_duplicate` PAIRS into a conservative set
of unique test-function deletion candidates.

Why pair count is not deletion count
-------------------------------------
A single test can participate in multiple duplicate pairs.

For example:

old-A -> middle-B
middle-B -> new-C

contains two removable pairs but only one final survivor is needed.

R3-3A therefore constructs directed coverage edges:

older test -> newer test

Only R3-2F-r1 rows with:
- decision = removable_duplicate
- deletion_authorized = true

are accepted as graph edges.

Safety rules
------------
- Tests appearing in `historical_keep` pairs are protected.
- Natural newer-side sinks are retained.
- A non-protected test is a deletion candidate only if an authorized directed
  path reaches a retained survivor.
- Directed cycles keep at least one canonical survivor.
- Canonical preference uses the later Phase number, then stable test ID order.

R3-3A does NOT delete anything.

Before actual deletion, R3-3B must still audit:
- file-level helper use,
- imports/constants used by retained tests,
- cross-test imports,
- whether deleting a whole file is safe versus deleting only selected
  functions.

Boundary
--------
- production changes: none
- existing-test changes: none
- deleted tests: 0
- repository-wide pytest: not run
