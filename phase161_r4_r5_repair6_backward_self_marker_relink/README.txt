Phase 161-R4-R5 repair6
Backward self-reference marker relocation

Audit finding
=============
The pipeline trace established the exact order:

Before reference-body consumer linking:
- R1 = Toda (5.2)
- R2 = Proposition 4.4
- R3 = Proposition 5.1

The body is ordered as:

  pi_4^3 = Z/2{eta_3}
  [R3]より, pi_{n+1}^n = Z/2{eta_n}

Therefore the concrete consumer occurs before the self-reference marker.

Repairs 3 and 4 only relocated a marker when the consumer was after the marker.
That condition prevented the correct Proposition 5.1 relocation.

Repair
======
Keep the existing graph-backed nearest-visible-consumer search.

For a self-reference marker:

  [Rn]より, <the Reference statement itself>

allow relocation to the unique visible consumer whether the consumer is before
or after the marker.

For legacy marker-only lines, keep the historical forward-only rule.

The repair4 zero-marker automatic linkage is removed because the runtime trace
showed that it incorrectly attached Proposition 4.4's R2 marker to the Toda
(5.2) line.

No pi_4^2-specific production condition is added.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py

New:
- tests/test_phase161_r4_r5_repair6_backward_self_marker_relink.py

Imports
=======
No production import changes.

Expected final public proof
===========================
Reference:
- R1 Toda (5.2), general form
- R2 Proposition 5.1, general higher-eta form

Body:
- [R2]より, pi_4^3 = Z/2{eta_3}.
- [R1]を i=4 に適用すると, eta_2 o -: pi_4^3 -> pi_4^2 は同型.
- eta_3 -> eta_2 eta_3.
- pi_4^2 = Z/2{eta_2^2}.
- QED

Full pytest is not run until Phase161 ends.
