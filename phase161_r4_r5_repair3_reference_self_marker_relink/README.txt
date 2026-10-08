Phase 161-R4-R5 repair3
Reference self-marker relink

Audit result
============
The public proof already has the correct general Proposition 5.1 Reference:

  pi_{n+1}^n = Z/2{eta_n}

The proof graph is also correct:

  Proposition 5.1 general component
    -> pi_4^3 specialization linkage
    -> pi_4^2 transport

The remaining defect is marker placement.

Current body:
  [R2]より, pi_{n+1}^n = Z/2{eta_n}.
  pi_4^3 = Z/2{eta_3}.

Required body:
  [R2]より, pi_4^3 = Z/2{eta_3}.

Design
======
Reuse the existing Phase154 graph-backed nearest-visible-consumer search.

Extend:
  link_toda_group_proof_narrative_reference_body_consumers()

It now handles two forms:

1. existing legacy marker-only line:
   [Rn]を用いる。

2. self-reference marker:
   [Rn]より, <the Reference statement itself>.

For case 2, when there is exactly one nearest visible non-root consumer,
the marker is moved to that consumer and the duplicate consumer line is removed.

No pi_4^2-specific string or rule-name condition is added.

Files
=====
Modified:
- toda_group_proof_narrative_contribution_renderer.py

New:
- tests/test_phase161_r4_r5_repair3_reference_self_marker_relink.py

Imports
=======
No production import changes.

Full replacement units are written to output/.

Completion criteria
===================
- Proposition 5.1 general statement remains in Reference.
- the same general statement is absent from proof body.
- concrete pi_4^3 remains in proof body.
- the Proposition 5.1 marker is attached to the pi_4^3 paragraph.
- Toda (5.2) remains.
- eta_3 -> eta_2 eta_3 remains.
- pi_4^2 conclusion and QED remain.
- existing Phase154/157 linkage regressions pass.

Full pytest is not run until Phase161 ends.
