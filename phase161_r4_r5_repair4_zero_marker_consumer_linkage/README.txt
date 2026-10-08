Phase 161-R4-R5 repair4
Zero-marker consumer linkage

Observed after repair3
======================
The general Proposition 5.1 statement is correctly removed from the proof body,
but the concrete pi_4^3 paragraph still has no [R2] marker.

This means the final linkage stage can receive a body where the Reference
marker has zero occurrences.

Repair
======
Extend the existing generic graph-backed function:

  link_toda_group_proof_narrative_reference_body_consumers()

Existing behavior remains:
- relocate a legacy marker-only line
- relocate a self-reference marker line

New behavior:
- when the marker has zero occurrences in the body
- and there is exactly one nearest visible non-root consumer
- attach the marker directly to that consumer

No pi_4^2-specific rule names, locators, or rendered math strings are used by
the production change.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py

New:
- tests/test_phase161_r4_r5_repair4_zero_marker_consumer_linkage.py

Imports
=======
No production import changes.

Expected public proof
=====================
Reference:
- (5.2) in general form
- Proposition 5.1 in general higher-eta form

Body:
- [R2]より, pi_4^3 = Z/2{eta_3}.
- [R1] applied at i=4
- eta_3 -> eta_2 eta_3
- pi_4^2 = Z/2{eta_2^2}
- QED

The full test suite is not run until Phase161 ends.
