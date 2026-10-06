Phase 159-R1-6d repair1

Scope
-----
Whitespace-only test-file repair.

Cause
-----
All R1-6d focused and related tests passed. The only failure was:

  tests/test_phase159_r1_6c_source_faithful_reference_linkage.py:
  new blank line at EOF.

Fix
---
Normalize the file ending to exactly one newline.

Production changes
------------------
None.

Test logic changes
------------------
None.

Full pytest
-----------
Not run.
