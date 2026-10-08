Phase 161-R4-R4
Restore global Reference frontier contract

Observed regression
===================
R4-R3 focused tests passed, but Phase156 frontier regressions showed that the
R4-repair1 change to the global Reference frontier was too broad.

Important failures:
- `(5.2)` disappeared from pi_6^3 frontier.
- pi_6^3 public Reference selection changed.
- downstream public headers changed.

R4-R4 design
============
Restore the global Reference frontier function to its existing Phase156-R13
contract.

Remove the early R4-only frontier filtering that was inserted immediately after
root-reference exclusion.

The pi_4^2 requirement is handled separately:

If the root is PROOF_INTERNAL and a FIXED_STATEMENT with the same literature
locator occurs in the root ancestry, that fixed statement is the public
literature boundary for the root transport.

Only the dependency closure used exclusively to prove that fixed statement is
treated as internal. Shared dependencies are retained.

For pi_4^2:
- root: proof-internal `(5.2)` finite-cyclic transport
- public fixed statement: `(5.2)` eta_2 composition isomorphism
- internal ancestry: Proposition 4.4 decomposition and its second-summand step

For pi_6^3:
- the global Phase156 frontier contract remains unchanged.

Changed production
==================
toda_group_proof_narrative_contribution_renderer.py

Changed functions:
- _toda_group_proof_narrative_reference_frontier_step_ids
- _toda_group_proof_narrative_reference_internal_step_ids
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown

New function:
- _toda_group_proof_narrative_root_fixed_statement_internal_step_ids

Removed R4 temporary helper:
- _filter_toda_group_proof_narrative_reference_entries_to_frontier
- _toda_group_proof_narrative_fixed_frontier_internal_step_ids

Imports
=======
No production import changes.

Tests
=====
New:
- tests/test_phase161_r4_r4_restore_global_frontier.py

Focused regression:
- Phase161 R4/R3/R1/R3 tests
- Phase156 R12/R13 frontier tests
- Phase156 R8 owned-ancestor tests, excluding one known stale assertion
- Phase59 relevant tests
- Phase160 k=2 tests

Known stale expectation
=======================
Phase156 repair8 still contains an assertion that the nu-prime definition
conclusion has `inference_rule is None`.

Current production explicitly attaches:
  Toda (5.3) nu-prime bracket definition

That historical assertion is not repaired in Phase161-R4.

Full pytest is not run until the end of Phase161.
