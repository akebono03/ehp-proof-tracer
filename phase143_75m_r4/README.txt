Phase 143-75M R4
================

Test-only repair.

R3 failed because its literal search string used the wrong escape form.
R4 locates the complete test function by its function definition and
replaces that whole function.

Production code is not changed.

Changed test function
---------------------
test_phase143_75m_prop511_renders_nu_squared_range

Expected
--------
5 passed

Production audit remains:
135 target occurrences
0 target rule-name fallback
0 errors
PASS

No full pytest suite is run.
