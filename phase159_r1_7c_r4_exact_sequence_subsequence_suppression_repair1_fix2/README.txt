Phase 159 R1-7c R4 exact-sequence subsequence suppression repair1 fix2

Purpose
-------
Narrow the repair1 suppression rule after the pi_6^3 existing exactness
regression showed that arbitrary containment was too broad.

Observed regression
-------------------
repair1 suppressed a required pi_6^3 exactness window because that window was
contained somewhere inside a longer displayed sequence.

Required pi_3^2 behavior
------------------------
The redundant sequence in pi_3^2 is different: it is the beginning of the
already displayed longer sequence.

Therefore the intended general rule is:

  suppress a shorter merged exactness sequence only when it is a strict
  prefix of a longer displayed exact sequence.

This preserves internal and suffix exactness windows.

Changed file
------------
toda_group_proof_narrative_contribution_renderer.py

Changed function
----------------
merge_toda_group_proof_narrative_adjacent_ehp_exactness_windows

No import changes.
No test changes.
No eta_2 wording changes.
No reference changes.
No generator canonicalization changes.

Focused verification
--------------------
1. pi_3^2 new focused regression
2. pi_6^3 existing exactness merge regression
3. generator canonicalization regression

Full pytest is intentionally not run.
