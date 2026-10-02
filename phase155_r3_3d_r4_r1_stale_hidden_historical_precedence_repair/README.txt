Phase 155-R3-3D-r4-r1 — stale hidden / historical precedence repair

Why r4 needed repair
--------------------
R3-3D-r4 activated six earlier same-name definitions because they contained
assertions not present in the final runtime definitions.

Focused pytest proved those assertions were not hidden current coverage.
They were stale expectations from an older set-rules contract:
- concrete `GroupMap.kernel_subgroup()` / `image_subgroup()` values were
  expected,
- while the current contract intentionally preserves symbolic
  `KernelSubgroupReference` / `ImageSubgroupReference` values.

Therefore these six tests must not be revived.

The r4 verifier also found two missing `historical_keep` IDs. Those IDs were
the two Phase41 older tests removed to resolve removable pairs. A single test
ID can participate in more than one pair classification, so the correct
precedence is:

`historical_keep` > `removable_duplicate`

when the same test ID participates in both classifications.

Changes
-------
- `tests/test_set_rules.py`
  - remove the six r4-created `*_phase155_hidden_coverage_1` tests.
  - keep the current canonical eight set-rule tests unchanged.
- `tests/test_phase41_preimage_subgroup.py`
  - restore the two historical_keep tests exactly from the r4 backup.
- production code: unchanged.
- imports: unchanged.

Verification
------------
Focused pytest covers:
- the eight current canonical set-rule tests,
- the two restored historical_keep Phase41 tests.

Closure checks require:
- six stale hidden tests absent,
- all historical_keep IDs present,
- original 161 safe deletion IDs still absent,
- no source-level duplicate test names,
- no unresolved removable pair except pairs overridden by historical_keep,
- focused pytest passes.

Repository-wide pytest is NOT run.
