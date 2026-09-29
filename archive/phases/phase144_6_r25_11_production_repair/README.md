# Phase 144-6 R25-11 Production Repair

## Scope

This repair restores the non-recursive semantic grouping key in
`toda_group_proof_narrative_contribution_ordering._group_key`.

The current `develop` implementation regressed to
`repr(occurrence.proof_step.conclusion)`, despite the retained R5-43-R2
contract requiring a normalized generic rendered statement.

## Production change

Only one production function is changed:

- `toda_group_proof_narrative_contribution_ordering._group_key`

No semantic-closure logic is changed.
No argument-builder logic is changed.
No connector-renderer logic is changed.
No expected population is updated.

## Expected verification

The focused run should establish whether restoring the retained grouping
invariant is sufficient to recover:

- Phase37 population: 353
- Phase38 population: 291
- Phase39 population: 194
- Phase40 / selected contribution population: 190
- pi_6^3 contribution count: 5
- detached selected contributions: 157
- detached insertable contributions: 0
- narrative-participating contributions: 33
- pi_6^3 connector behavior
- R25-9B depth=2 nu-prime definition visibility

If these recover, the apparent semantic-closure ownership leak was a
secondary symptom of the `_group_key` regression and no closure-specific
production change should be made in R25-11.

If any ownership failure remains after this repair, that remainder should
be isolated before changing semantic closure.
