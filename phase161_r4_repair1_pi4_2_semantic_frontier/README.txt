Phase 161-R4 repair1
pi_4^2 semantic specialization + fixed-statement frontier

Observed failure
================
R4 focused tests:
- specialization plan returned None
- Proposition 4.4 remained public

Root cause 1
============
Toda52CompositionIsomorphismStatement does not have a `map` field.

Its runtime structure is:

  source_group
  target_group
  composition

The original R4 specialization helper incorrectly read `statement.map`.

Root cause 2
============
The existing Reference frontier traversal allowed a dependency to pass through
a child reference when that child reference had the same locator as the root.

For pi_4^2:
- root `(5.2)` is PROOF_INTERNAL
- direct `(5.2)` composition isomorphism is FIXED_STATEMENT
- Proposition 4.4 is an internal proof dependency of that fixed statement

Therefore the fixed `(5.2)` must be a public boundary. Traversal from
Proposition 4.4 must stop there.

Changes
=======
Modified:
- toda_group_proof_narrative_contribution_renderer.py

Changed functions:
- _toda_group_proof_narrative_reference_frontier_step_ids
- _toda_group_proof_narrative_fixed_composition_isomorphism_specialization_plan
- render_toda_group_proof_narrative_multi_argument_with_contributions_markdown

New function:
- _filter_toda_group_proof_narrative_reference_entries_to_frontier

New test:
- tests/test_phase161_r4_repair1_pi4_2_semantic_frontier.py

Imports
=======
No import changes.

Expected public proof boundary
==============================
Reference:
  (5.2) in general form.

Proof body:
  specialize (5.2) at i=4,
  use pi_4^3 = Z/2{eta_3},
  show generator transport,
  conclude pi_4^2 = Z/2{eta_2^2}.

Proposition 4.4 remains an internal dependency of the fixed `(5.2)` statement.

Tests
=====
Focused:
- Phase161 R4 repair1
- Phase161 R4
- Phase161 R3

Regression:
- Phase156 reference frontier tests
- Phase59 relevant tests
- Phase160 k=2 transport tests

Full suite is NOT run in this repair.
