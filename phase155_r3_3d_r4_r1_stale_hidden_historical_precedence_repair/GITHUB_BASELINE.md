# GitHub baseline — Phase 155-R3-3D-r4-r1

Repository: `akebono03/ehp-proof-tracer`
Branch: `main`
Observed public baseline commit: `8301520a7434f3836b1dbc7e8fa08a60c024225a`

Before this repair, current GitHub code/tests were re-inspected for:
- `tests/test_set_rules.py`,
- `set_rules.py`,
- `tests/test_phase41_preimage_subgroup.py`.

The current set-rules contract uses symbolic `KernelSubgroupReference` and
`ImageSubgroupReference` terms rather than eagerly replacing them with the
concrete `GroupMap.kernel_subgroup()` / `image_subgroup()` values expected by
the six revived historical tests.

The r4 focused failures therefore identify stale shadowed expectations, not
missing current coverage.

The two removed Phase41 IDs also belong to historical_keep classifications.
R3-3D-r4-r1 restores those exact tests and applies historical_keep precedence
when pair classifications overlap.

No production code is changed and repository-wide pytest remains deferred to
Phase 155 closure.
