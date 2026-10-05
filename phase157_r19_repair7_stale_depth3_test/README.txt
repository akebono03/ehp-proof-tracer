Phase157-R19 repair7

Purpose
-------
Update one stale Phase157-R3 test contract.

Current public proof behavior is intentional:
- Proposition 5.3 is a public Reference.
- Its internal depth-3 derivation step
    E: pi_4^2 -> pi_5^3
  should not leak into the public proof body.
- The public proof instead uses the specialized consequence
    pi_7^5 = Z/2{eta_5^2}
  through [R3].

Changed file
------------
tests/test_phase157_r3_pi6_3_reference_boundary.py

Changed test
------------
test_phase157_r3_pi6_3_depth3_keeps_prop53_derived_suspension_in_body
becomes
test_phase157_r3_pi6_3_depth3_suppresses_prop53_internal_suspension

Production code changes: none
Import changes: none
Documentation changes: none
Repository-wide pytest: not run
