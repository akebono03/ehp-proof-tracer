Phase 159-R1-6d repair2

Purpose
-------
Move the Toda (5.1) target-group fact to the point where it is actually needed.

For pi_3^2 the public order becomes:

  Delta is zero.
  H is surjective. (2)
  [R1] pi_3^3 = Z{iota_3}.
  From (1) and (2), H is an isomorphism.
  Define eta_2 as the unique preimage of iota_3.

Implementation
--------------
The renderer does not hard-code pi_3^3. It matches:
- a TodaHopfInvariantSurjectiveStatement,
- its target group,
- a Toda (5.1) referenced Relation whose left side is that target group.

Only public proof order is changed.

Full pytest
-----------
Not run.
