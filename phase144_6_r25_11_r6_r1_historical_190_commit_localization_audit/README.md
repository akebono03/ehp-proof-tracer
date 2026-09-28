# Phase 144-6 R25-11-R6-R1 Historical 190 Commit Localization Audit

## Purpose

Locate a real historical Git commit that reproduces the retained
190-contribution six-group baseline.

R25-11-R6 proved that commit
`af2e259b55fcfa7cf204fdcb50d5194bb2232bd0` reproduces 145 rather than 190.
Therefore it cannot be used as the historical side of a 190-to-192 exact-delta
comparison.

## Files, classes, functions, and methods

Production files changed: none.

Existing tests changed: none.

Audit-only files added:

- `collect_selected_total.py`
- `locate_historical_190.ps1`
- `test_phase144_6_r25_11_r6_r1.py`
- `run_phase144_6_r25_11_r6_r1.ps1`
- `README.md`

The collector exercises the existing six-group production route through:

- `render_toda_group_proof_narrative_multi_argument_markdown`
- `build_toda_group_proof_narrative_ordered_contributions`
- the retained Phase 144-6 R5-18 six-group `_context`

## Candidate selection

The locator obtains commits from local Git history that changed one or more
Narrative production files involved in selection, ownership, visibility,
rendering, semantic closure, or insertion.

It does not hard-code a guessed historical 190 SHA.

## Measurement

Each candidate is checked in a detached temporary Git worktree.

The six representative groups are:

- pi_6^3
- pi_8^5
- pi_10^4
- pi_12^5
- pi_15^8
- pi_16^9

A candidate is accepted only when its own historical production code actually
returns selected total 190.

Commits whose historical checkout predates the retained R5-18 foundation or
cannot execute the collector are reported as unavailable rather than treated
as evidence.

## Cache

Population measurements are appended to `population_cache.tsv`.

Rerunning the audit reuses completed measurements instead of rebuilding those
worktrees.

## Completion conditions

R25-11-R6-R1 completes only when at least one real historical commit reproduces
selected total 190. The output reports the exact SHA, subject, six-group
population, and neighboring measurable commits.

If no candidate reproduces 190, the audit exits without making a historical
190-to-192 delta claim.

## Next boundary

After an exact-190 SHA is established, R25-11-R6 can be rerun with that SHA to
compute the exact semantic Counter delta against the current 192 checkout.

No production repair is made here.

No full pytest is run.
