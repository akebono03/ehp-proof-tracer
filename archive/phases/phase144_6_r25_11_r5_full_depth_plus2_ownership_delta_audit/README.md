# Phase 144-6 R25-11-R5 Full-Depth +2 Ownership Delta Audit

## Purpose

Identify the structural location of the two extra selected contributions in
the current full-depth six-group ownership population.

R25-11-R4 established that semantic closure is not the cause of the
192-versus-190 regression. R25-11-R5 therefore excludes semantic closure from
the diagnosis.

## Files, classes, functions, and methods

Production files changed: none.

Existing tests changed: none.

Audit-only files added:

- `audit_r25_11_r5.py`
- `test_phase144_6_r25_11_r5.py`
- `run_phase144_6_r25_11_r5.ps1`
- `README.md`

Production functions inspected before this audit:

- `build_toda_group_proof_narrative_ordered_contributions`
- `_build_visibility_occurrences`
- `_group_key`
- `_owner`
- `_contribution_insertion_indices`

Related retained tests inspected:

- `tests/test_phase144_6_r5_40_narrative_contribution_placement_order_audit.py`
- `tests/test_phase144_6_r5_43_11c_r2_argument_participation_guard.py`
- `tests/test_phase144_6_r5_43_11d_final_completion_audit.py`

## Retained baseline

The audit does not rebase expected values.

- selected total: 190
- pi_6^3 selected: 5
- Narrative-participating selected: 33
- detached selected: 157
- detached insertable: 0

## Audit sections

### A. Full-depth selected population delta

Reports the current selected population for all six representative groups.

### B. Participation and insertion-boundary delta

Reports current participating/detached counts and prints every detached
contribution that is currently insertable.

### C. pi_6^3 selected ownership inventory

Prints all six current pi_6^3 selected contributions with argument role,
discourse role, statement type, rule, provider-anchor status, placement,
provider-key count, distance and insertion status.

### D. Candidate +2 ownership-delta summary

Reports participating and detached-insertable counts per group.

This is a structural diagnosis. It does not assume that all detached-insertable
rows are themselves the two extra selected rows.

## Performance

Each of the six full-depth contexts is built once. The resulting inventory is
reused by Sections A-D. Phase37-40 and the full test suite are not run.

## Completion conditions

R25-11-R5 is complete when the output identifies:

- which groups contain the participation/insertion anomalies;
- the exact pi_6^3 six-row ownership inventory;
- all detached contributions that became insertable;
- the group distribution needed to design the minimal general repair.

## Next boundary

No production ownership rule is changed in R25-11-R5.

R25-11-R6 may make a minimal production repair only after the R25-11-R5 output
shows a general structural condition. It must not hard-code pi_6^3, a specific
Toda rule name, or a specific statement class.

No full pytest is run in R25-11-R5.
