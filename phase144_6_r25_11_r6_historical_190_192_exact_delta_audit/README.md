# Phase 144-6 R25-11-R6 Historical 190->192 Exact Delta Audit

## Purpose

Compute the exact semantic delta between a real historical 190-contribution
checkout and the current 192-contribution checkout.

R25-11-R5 established that the current population is 192, with 35
Narrative-participating and 157 detached contributions. This audit does not
guess which two rows are new.

## Historical source

The audit uses commit:

`af2e259b55fcfa7cf204fdcb50d5194bb2232bd0`

GitHub identifies this commit as `Phase144-6-Repair`. It precedes the later
R25-9A and R25-9B changes involved in the current regression investigation.

The runner creates a temporary detached Git worktree at that exact commit and
executes the same inventory collector against the historical production code.

The comparison is allowed to continue only if that checkout actually produces
190 selected contributions. If it does not, the audit stops and makes no
190-to-192 delta claim.

## Files, classes, functions, and methods

Production files changed: none.

Existing tests changed: none.

Audit-only files added:

- `collect_r25_11_r6_inventory.py`
- `compare_r25_11_r6.py`
- `test_phase144_6_r25_11_r6.py`
- `run_phase144_6_r25_11_r6.ps1`
- `README.md`

Current and historical production paths exercised include:

- `build_toda_group_proof_narrative_ordered_contributions`
- `render_toda_group_proof_narrative_multi_argument_markdown`
- `_contribution_insertion_indices`
- argument discourse classification
- the retained six-group `_context` foundation

## Semantic identity

Cross-checkout object IDs and provider block IDs are intentionally excluded.

A selected contribution is compared by:

- group `(n, k)`
- argument role
- discourse role
- statement type
- normalized generic rendered statement
- provider-anchor flag
- placement
- provider-key count

Insertability is compared separately so that a retained semantic contribution
whose insertion state changed is reported as an insertion-state change rather
than as an artificial remove/add pair.

Multiplicity is preserved with `collections.Counter`.

## Audit sections

### A. Historical baseline validation

Requires the historical checkout to reproduce exactly 190 selected
contributions.

### B. Exact semantic selected-set delta

Prints all added and removed semantic signatures with multiplicity.

### C. Insertion-state changes

Prints retained semantic signatures whose insertion status changed between the
historical and current checkout.

### D. Exact-delta completion guard

Requires the Counter difference to explain a net `+2`.

## Performance

The six representative full-depth contexts are built once in the historical
worktree and once in the current checkout.

No Phase37-40 regression bundle is run.

No full pytest is run.

## Completion conditions

R25-11-R6 is complete only if:

1. the historical commit reproduces selected total 190;
2. the current checkout reproduces selected total 192;
3. the exact added/removed semantic Counter delta has net `+2`;
4. insertion-state changes are reported independently.

## Next Phase boundary

R25-11-R6 makes no production repair.

A following repair may be designed only from the exact historical/current
structural delta. It must remain generic and must not hard-code a group,
specific Toda rule name, or specific statement class.
