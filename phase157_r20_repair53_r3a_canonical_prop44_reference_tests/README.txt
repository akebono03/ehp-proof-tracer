Phase157-R20 repair53-r3a — Canonical Proposition 4.4 Reference tests

Observed repair53-r3 result
---------------------------
The first three focused tests passed:
1. n=8 Prop44 step is FIXED_STATEMENT / Proposition 4.4.
2. extracted Reference identity is Proposition 4.4.
3. graph Reference entries split Proposition 4.4 from Proposition 5.15.

The fourth test failed only because it required the historical dedicated
renderer title:

  Toda Proposition 4.4 の分解同型

Current Phase157 public Reference rendering uses the canonical locator title:

  **[R#] Proposition 4.4.**

This is intentional shared Reference-renderer behavior.

Changed files
-------------
Test-only:
- tests/test_phase134_24_pi15_8_narrative.py
- tests/test_phase150_rc4_7a_cross_group_reference_normalization.py
- tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py

Changed functions
-----------------
- test_phase134_24_pi15_8_narrative_has_mathematical_structure()
- test_phase150_rc4_7a_pi15_8_special_renderer_is_unchanged()
- test_phase157_r20_repair53_r3_public_pi15_8_restores_prop44_reference()

New contract
------------
The tests still require Proposition 4.4 to be visible and mathematically
identified by its decomposition-isomorphism statement, but no longer require
the Phase134-only prose title.

They require:
- canonical Proposition 4.4 Reference title;
- the decomposition-isomorphism formula;
- existing pi_15^8 prose behavior where applicable.

Production code changes
-----------------------
None.

Import changes
--------------
None.

Then repair53-r3 validation resumes:
- focused attribution/pi15 tests;
- repair53 fragment tests;
- recent Phase157 regressions;
- residual 112-group audit;
- final pi_15^8 Reference section printout.

Repository-wide pytest remains deferred to Phase157 closure.
