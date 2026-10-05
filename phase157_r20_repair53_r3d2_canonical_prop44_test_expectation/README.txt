Phase157-R20 repair53-r3d2
canonical Proposition 4.4 test expectation repair

Reason for r3d2
---------------
repair53-r3d failed before changing any file because its apply script
looked for an incorrectly escaped source fragment.

The real test source contains:

  r"\left(α, \beta\right) \mapsto "
  r"Eα + \sigma_{8}\beta"

The r3d apply script searched for a different escaped string and
therefore reported zero matches.

r3d2 fixes only the package/apply logic.

Target change
-------------
Test file only:

  tests/test_phase157_r20_repair53_r3_fixed_reference_attribution.py

Old assertion fragment:

  r"\left(α, \beta\right) \mapsto "
  r"Eα + \sigma_{8}\beta"

New canonical assertion fragment:

  r"(α, \beta) \mapsto "
  r"Eα + \sigma_{8}\beta"

Production changes
------------------
None.

Imports
-------
No changes.

Verification
------------
- compile changed test
- print the complete changed test function
- confirm stale \left(...\right) expectation is absent
- confirm canonical (...) expectation is present
- run repair53-r3 fixed-attribution tests
- run repair53-r3c marker-remapping tests

Repository-wide pytest is not run.
