# Phase 159 R1-7c R4 repair6

## Exactness range fix

The local source inspection confirmed the nested `exactness_reason()` body:

- starts at the local `def exactness_reason(`,
- ends before `candidate_zero_steps = []`,
- contains exactly one `+ "$ である."` closing line.

Repair5 failed because it treated the multiline function signature continuation
`) -> str | None:` as the end of the nested function.

Repair6 instead uses the stable semantic range from `def exactness_reason(` to
`candidate_zero_steps = []` and changes only the exact closing line:

`+ "$ である."`

to:

`+ "$."`

Previously applied Phase159 proof-body normalization and its connection are
preserved.

## Import changes

None.

## Verification

- syntax check for the four affected production modules,
- Phase150 focused renderer regressions,
- Phase157 focused prose/order regressions,
- Phase159 R4 repair6 focused regression,
- R4 cross-group re-audit.

Repository-wide pytest is intentionally not run.
