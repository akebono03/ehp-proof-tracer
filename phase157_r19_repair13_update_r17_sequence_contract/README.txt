Phase157-R19 repair13

Purpose
-------
Update one stale Phase157-R11/R17 test contract.

Current intended behavior
-------------------------
The initial proof now uses one full EHP exact sequence:

  pi_7^3 --H--> pi_7^5 --Delta--> pi_5^2 --E--> pi_6^3

The old shorter fragment

  pi_7^5 --Delta--> pi_5^2 --E--> pi_6^3

should no longer be rendered separately.

The later group-structure sequence remains trimmed to:

  pi_5^2 --E--> pi_6^3 --H--> pi_6^5

Changed file
------------
tests/test_phase157_r11_r17_residual_narrative_defects.py

Production code changes: none
Import changes: none
Documentation changes: none
Repository-wide pytest: not run
