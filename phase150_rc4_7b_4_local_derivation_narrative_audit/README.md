# Phase 150 RC4-7B-4 Local-Derivation Narrative Audit

This package is audit-only. It does not change production code or existing tests.

## Purpose

RC4-7B-3 showed 180 `TARGET_LOCAL_DERIVATION_HANDOFF` candidates and zero transitive-external handoffs.

RC4-7B-4 therefore audits the existing generic `DERIVATION` transitions rather than changing `child_argument_indices`.

For each representative group it reports:

- the Argument owning the derivation,
- the existing transition source blocks,
- whether each source is already in the target Argument local body,
- whether source facts and the conclusion are visible in the rendered Narrative,
- the complete target local body in dependency order,
- a visibility classification.

The representative groups are:

- pi_10^4
- pi_12^5
- pi_15^8 (positive control)
- pi_16^9

## Classification

- `VISIBLE_LOCAL_DERIVATION`
  - all transition sources are in the target local body,
  - at least one source is visible in the rendered Narrative,
  - the conclusion is visible.

- `HIDDEN_SOURCE_LOCAL_DERIVATION`
  - all transition sources are in the target local body,
  - the conclusion is visible,
  - source facts are not visible.

- `PARTIAL_LOCAL_DERIVATION`
  - the conclusion is visible, but not all transition sources are in the local body.

- `NONVISIBLE_DERIVATION`
  - the conclusion is not visible.

## Boundary

This audit does not:

- add or change Argument ownership,
- change `child_argument_indices`,
- change local-body extraction,
- change renderer prose,
- add group-specific branches,
- run the repository-wide test suite.

A production repair is considered only after this audit identifies which existing local derivations need generic prose assembly.
