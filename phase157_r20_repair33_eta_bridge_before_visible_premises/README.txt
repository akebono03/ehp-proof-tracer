Phase157-R20 repair33

Purpose
-------
Place adjacent eta-suspension bridges before visible direct premises that use
those eta definitions.

Current failure
---------------
After repair32, the full exactness statement is correctly placed before the
eta_6 bridge.

However the body still has:

  [R5] Proposition 2.2 support
  eta_6 = E eta_5
  H(nu' eta_6) = eta_5^2

The mathematical dependency order should be:

  eta_6 = E eta_5
  [R5] Proposition 2.2 support
  H(nu' eta_6) = eta_5^2

Generic rule
------------
For a consumer step with at least two adjacent eta-family definition premises:
1. locate the visible consumer;
2. locate visible non-definition direct premises of that consumer that already
   occur before the consumer;
3. insert the eta bridge before the earliest of those visible direct premises;
4. if no such premise exists, retain the old behavior and insert immediately
   before the consumer.

This is dependency-based and does not inspect proposition numbers, group
dimensions, generator names, or pi_6^3.

Changed production file
-----------------------
- toda_group_proof_narrative_contribution_renderer.py

Changed function
----------------
- insert_toda_group_proof_narrative_adjacent_eta_suspension_bridges()

New test
--------
- tests/test_phase157_r20_repair33_eta_bridge_before_visible_premises.py

Completion condition
--------------------
- full exactness < eta bridge < visible fixed-reference premise < consumer;
- repair32 exactness anchoring remains intact;
- Phase157 regressions proceed to the next independent defect.

No documentation changes.
No repository-wide pytest.
