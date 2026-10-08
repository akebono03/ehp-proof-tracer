Phase 161-R4-R4 repair2
Align the new frontier regression test with the existing Phase156 contract.

Observed failure
================
The new R4-R4 test expected `Lemma 5.4` to be on the pi_6^3 frontier, but its
own test helper first applied:

  filter_toda_group_proof_narrative_reference_entries_by_fixed_statement_boundary

The historical Phase156-R12/R13 frontier tests do not apply that filter before
calling `_toda_group_proof_narrative_reference_frontier_step_ids`.

Therefore the R4-R4 test was not testing the same contract it claimed to
restore.

Repair
======
Production code is unchanged.

The test now uses two explicit entry paths:

1. pi_4^2 public rendering path
   - fixed-statement boundary filter
   - root exclusion

2. Phase156 global frontier contract path
   - build reference entries
   - root exclusion
   - frontier helper

This preserves the distinction between:
- production fixed-statement selection
- the lower-level global frontier helper contract

Files
=====
Updated:
- tests/test_phase161_r4_r4_restore_global_frontier.py

Production changes:
- none

Full suite:
- not run
