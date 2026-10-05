Phase157-R20 repair53-r3d3
canonical Proposition 4.4 audit-script fix

Current state
-------------
repair53-r3d2 successfully changed the existing test expectation to:

  r"(α, \beta) \mapsto "
  r"Eα + \sigma_{8}\beta"

The failure occurred only in the r3d2 audit script.

Cause
-----
The audit compared the source text of the Python test function against
the concatenated runtime string value. Therefore it reported the
canonical expectation as missing even though the printed function
showed it was present.

r3d3
----
No production code changes.
No test changes.

The audit now compares the exact two source-code lines:

  r"(α, \beta) \mapsto "
  r"Eα + \sigma_{8}\beta"

and confirms the stale source form with \left / \right is absent.

Verification
------------
1. Compile the existing modified test.
2. Audit the exact source-code lines.
3. Run repair53-r3 fixed-attribution tests.
4. Run repair53-r3c marker-remapping tests.

Repository-wide pytest remains reserved for the end of Phase 157.
