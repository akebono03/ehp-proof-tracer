Phase 159 R1-7c R4 exact-sequence suppression repair2 fix2

Cause
-----
repair2 fix1 successfully added the late suppression helper and its call,
but it did not restore the early merge helper modified by repair1/fix2.

Therefore pi_6^3 still lost its required exactness sequence before the late
suppression stage.

Fix
---
Restore:
  merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows()

to the current GitHub implementation.

Keep unchanged:
  suppress_toda_group_proof_narrative_late_exact_sequence_prefix_restatements()

and its late call in the public contribution renderer.

Expected behavior
-----------------
pi_3^2:
- long sequence appears first in final Narrative;
- later shorter prefix is suppressed.

pi_6^3:
- earlier exactness statement is preserved;
- later longer sequence is also preserved.

No eta_2 wording changes.
No Reference changes.
No generator changes.
No full pytest.
