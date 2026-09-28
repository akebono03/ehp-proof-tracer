# Phase 144-6 R25-10-R3 — Contribution Import Repair

## Purpose

Repair one incorrect import in the R25-10 diagnostic script.

The current Phase 144-6 test
`tests/test_phase144_6_r5_43_r2_recursive_repr_repair.py` imports
`build_toda_group_proof_narrative_ordered_contributions` from:

`toda_group_proof_narrative_contribution_ordering`

The original R25-10 audit incorrectly imported it from the nonexistent
`toda_group_proof_narrative_contributions` module.

## Changed audit code

Only the import source for
`build_toda_group_proof_narrative_ordered_contributions` is changed.

## Production changes

None.

## Existing test changes

None.

## Execution environment

The R25-10-R2 execution environment is retained:

- repository root is on `PYTHONPATH`;
- repository `tests` directory is on `PYTHONPATH`;
- stdout and stderr are captured to the audit output file through `cmd /c`.

## Full suite

Not run. This remains an ownership audit only.

## Completion condition

The runner must reach:

`R25-10-R3 RESULT: PASS`

The resulting audit output should then identify the remaining contribution,
detached-boundary, connector, and recursive-repr ownership needed before a
minimal production repair is selected.
