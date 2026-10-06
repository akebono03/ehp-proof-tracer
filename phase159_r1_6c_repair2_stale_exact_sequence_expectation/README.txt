Phase 159-R1-6c repair2

Scope
-----
Test-only repair.

Reason
------
R1-6c intentionally removes the redundant "は完全である." suffix when the
preceding prose already says "次の完全列を考える."

The old R1-4 test still expected that suffix.

The repaired test keeps the original structural requirement:
exactly one public exact-sequence line is present.

It additionally asserts that the redundant exactness prose is absent.

Production changes
------------------
None.

Full pytest
-----------
Not run.
