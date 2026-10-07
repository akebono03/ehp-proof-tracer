Phase 159 R1-7c R4 generator canonicalization repair1 fix2

Purpose
-------
Remove one stale explicit-marker ordering expectation.

Current contract
----------------
The current design explicitly allows structural Reference attribution without
an explicit [Rk] marker in the proof body. Therefore presence of the selected
Reference entry does not imply that the body must contain "[R5]より".

Observed runtime
----------------
The current public pi_6^3 Narrative contains the five selected references:
- Proposition 5.6
- (5.3)
- Proposition 5.3
- Proposition 5.1
- (5.7)

The only failing assertion required:
  [R5]より
to occur before:
  [R3]より

That is no longer a valid invariant.

Changes
-------
Production code changes: none.

Modified:
tests/test_phase157_r20_generic_dependency_rendering.py

The test still verifies that all five current references are present.
It no longer requires an explicit R5 body marker or an ordering relation
between explicit R5 and R3 markers.

Focused verification
--------------------
- tests/test_phase157_r20_generic_dependency_rendering.py
- tests/test_phase159_r1_7c_r4_generator_canonicalization_repair1.py
- tests/test_phase143_3_generic_eta_normalization.py
- tests/test_phase59_prop53_integration.py

Full pytest is intentionally not run.
