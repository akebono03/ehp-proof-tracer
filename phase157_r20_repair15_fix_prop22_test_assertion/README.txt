Phase157-R20 repair15

Purpose
-------
Fix one invalid test assertion introduced by repair10.

Failure
-------
The test used:

  assert "lpha" not in r5

That assertion also fails for the correct LaTeX string `\alpha`, because the
substring `lpha` is naturally contained in `alpha`.

Evidence
--------
The immediately preceding assertion already passed:

  assert r"H(\alpha\circ E\beta)" in r5

Therefore the production Proposition 2.2 Reference rendering is correct.

Change
------
Replace the invalid substring assertion with explicit checks that:
- `\alpha` is present;
- `\beta` is present;
- malformed `H(lpha...` forms are absent.

Changed file
------------
- tests/test_phase157_r20_repair10_reference_local_specialization.py

Changed function
----------------
- test_phase157_r20_repair10_public_references_are_dependency_specialized()

Production code changes: none.
Documentation changes: none.
Repository-wide pytest: not run.
