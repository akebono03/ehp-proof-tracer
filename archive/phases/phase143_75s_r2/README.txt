Phase 143-75S-R2
================

Purpose
-------
Repair only the missing test-file placement from the Phase 143-75S ZIP.

Cause
-----
The original Phase 143-75S archive contained the focused test inside
phase143_75s, but run_phase143_75s.ps1 expected the same file under tests.

Production changes
------------------
None.

Repair
------
Copy:

phase143_75s/test_phase143_75s_toda58_whitehead_square_semantic_rendering.py

to:

tests/test_phase143_75s_toda58_whitehead_square_semantic_rendering.py

Then run the three focused tests and repeat the target audit.

Completion criteria
-------------------
3 passed

target aggregate components: 45
semantic renderings: 45
None renderings: 0
errors: 0
PASS

No full pytest
--------------
The full suite remains deferred until the end of Phase 143.
