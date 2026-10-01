Phase 153 R13 Closure Verification
====================================

Purpose
-------
Verification-only package after the R13 syntax repair.

Production changes
------------------
None.

Checks
------
1. Phase 153 focused regression:
   R8, R9, R10, R11, R12, R13, R13 syntax repair, and pi15_8 specialized
   Narrative tests.

2. 112-group closure audit:
   n = 2..15
   k = 0..7
   depth = 2

Completion condition
--------------------
- focused pytest passes;
- scanned groups = 112;
- render errors = 0;
- Reference invariant violations = 0.

If all conditions pass, the next step is the Phase 153 final full pytest.

Punctuation normalization and proof-prose cleanup remain Phase 154 work.
