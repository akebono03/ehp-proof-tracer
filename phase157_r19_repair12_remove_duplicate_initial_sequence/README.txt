Phase157-R19 repair12

Purpose
-------
repair11 correctly added:
- the full EHP exact sequence,
- eta_6 = E eta_5,
- the explicit Proposition 2.2 calculation,
- ker Delta = Im H = pi_7^5.

Only one duplicate remained:
  pi_7^5 --Delta--> pi_5^2 --E--> pi_6^3

Cause
-----
The repair11 helper used exact paragraph equality for the short initial
sequence. The actual rendered paragraph survived that equality check.

Change
------
Replace exact equality with a bounded substring test and remove only the
short initial EHP fragment. The full exact sequence remains.

Changed file
------------
- toda_group_proof_narrative_contribution_renderer.py

No import changes.
No test changes.
No Reference changes.
No documentation changes.
No repository-wide pytest.
