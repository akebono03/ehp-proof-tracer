# Phase 159 R1-7c R4 repair5

## Exactness-function recovery

Repair4 successfully connected the Phase159 proof-body normalizer and then
stopped while trying to update the hidden zero-map exactness prose.

Repair5 preserves that successful connection.

Instead of matching the entire source fragment, repair5 locates the nested
`exactness_reason` function inside
`toda_group_proof_narrative_contribution_renderer.py` and changes only its
closing mathematical prose from:

`+ "$ である."`

to:

`+ "$."`

The related stale expectations are updated idempotently.

## Import changes

None.

## Verification

- `py_compile` for the four affected production modules
- Phase150 focused renderer regressions
- Phase157 focused prose/order regressions
- Phase159 R4 repair5 focused regression
- R4 cross-group re-audit

Repository-wide pytest is intentionally not run.
