Phase 159 R1-7c R4 generator canonicalization repair1 fix1

Purpose
-------
Complete the partially applied repair1 safely.

Observed state after the first repair1 run
------------------------------------------
The first apply script changed the production renderer before it failed while
trying to replace a stale Phase 143 test.

Evidence from the user's runtime output:
- public Proposition 5.3 already renders
  pi_7^5 = Z/2{eta_5^2};
- the old pi_7^5 = Z/2{eta_5 eta_6} form is no longer shown there.

Therefore fix1 does NOT apply another production change. It verifies that the
repair1 production helper/fallback is already present and aborts if it is not.

Files changed by fix1
---------------------
1. tests/test_phase143_3_generic_eta_normalization.py
2. tests/test_phase157_r20_generic_dependency_rendering.py
3. tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py
   (new/refreshed)

Stale expectation repairs
-------------------------
Phase 143:
The derivation equality eta_3 eta_4 eta_5 = eta_3^3 is intentionally visible
under the later contract. The old requirement that the expanded chain never
appear in any step is removed.

Phase 157 reference contract:
The old R5 expectation Proposition 2.2 is replaced with the current fixed
locator (5.7).

Phase 157 eta contract:
The fixed literature statement (5.3) may legitimately contain
eta_3 eta_4 eta_5. The regression now forbids the unwanted group-generator
display

  pi_7^5 = Z/2{eta_5 eta_6}

while requiring eta_5^2.

No production code is changed by fix1.
No full pytest is run.
