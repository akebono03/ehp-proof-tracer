Phase 161-R4-R4 repair1
Update superseded R4-R3 test

Observed failure
================
R4-R4 removed temporary R4-R3 helpers:

- _filter_toda_group_proof_narrative_reference_entries_to_frontier
- _toda_group_proof_narrative_fixed_frontier_internal_step_ids

The older R4-R3 focused test still imported those helpers, so pytest failed
during collection before any test ran.

Repair
======
Update only:

  tests/test_phase161_r4_r3_fixed_frontier_internal_ancestry.py

The test now uses the current R4-R4 contract:

- _toda_group_proof_narrative_root_fixed_statement_internal_step_ids
- _toda_group_proof_narrative_reference_internal_step_ids
- the restored global _toda_group_proof_narrative_reference_frontier_step_ids

No production code is changed.

Imports
=======
The test import section is replaced in full by the new test file.

Test policy
===========
The public specialized map is tested semantically:
- [R1]
- i=4
- pi_4^3 -> pi_4^2
- isomorphism

The Proposition 4.4 general decomposition and second-summand prose must remain
absent from the pi_4^2 public body.

The full test suite is not run.
