Phase157-R20 repair53-r3d
canonical Proposition 4.4 test expectation repair

Diagnosis
---------
repair53-r3c production behavior is correct:

  3 passed

The remaining repair53-r3 failure expects:

  \left(α, \beta\right) \mapsto Eα + \sigma_{8}\beta

However, the current canonical generic Reference statement renderer
for TodaProp44IsomorphismStatement explicitly renders:

  (α, \beta) \mapsto Eα + \sigma_{8}\beta

without \left and \right.

Therefore the remaining failure is a stale test expectation, not a
production Reference attribution or numbering defect.

Change
------
Test-only replacement in:

  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py

Old expectation:

  r"\left(α, \beta\right) \mapsto "
  r"Eα + \sigma_{8}\beta"

New expectation:

  r"(α, \beta) \mapsto "
  r"Eα + \sigma_{8}\beta"

No production code is changed.
No imports are changed.
No fixed-statement classification is changed.
No Reference identity is changed.
No graph entry is changed.
No Reference marker remapping is changed.

Verification
------------
1. Compile the modified test.
2. Print the complete modified test function.
3. Verify the stale \left(...\right) expectation is absent.
4. Verify the canonical (...) expectation is present.
5. Run the repair53-r3 fixed-attribution test file.
6. Run the repair53-r3c marker-remapping test file.

Repository-wide pytest remains reserved for the end of Phase 157.
