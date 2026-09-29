Phase 143-75M R3
================

This is a test-only repair.

Production code
---------------
No production file is changed.

Reason
------
Phase 143-75M R2 production rendering is correct:
the runtime semantic statement contains higher_range n >= 9.

The R2 focused test incorrectly expected n >= 5.

Current repository evidence also treats the symbolic
Toda Proposition 5.11 nu-squared specialization as n >= 9,
including the existing Phase 74 test named:

test_phase74_5_prop511_higher_range_is_n_at_least_9

Changed test function
---------------------
test_phase143_75m_prop511_renders_nu_squared_range

Expected
--------
5 passed

Then the existing Phase 143-75M R2 production audit should still report:
135 target occurrences
0 target rule-name fallback
0 errors
PASS

No full pytest suite is run.
