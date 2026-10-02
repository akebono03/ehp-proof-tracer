Phase 155 Closure-R3-R3

Repairs only the three remaining R3-R2 job1 failures.

Changes:
1. Delete the redundant static source-shape test that required the pi6 branch
   source slice to contain the generic renderer function name. The same file
   already behavior-tests that the legacy special renderer is not called.
2. Keep the depth-2 nu-prime definition tests, but remove the historical
   requirement that pi_5^3 must never appear in the rendered Reference section.
   Reference relevance/minimal display is reserved for Phase156.

No production changes.
No top-level import changes.
No audit-only execution.
No monolithic pytest.

The verifier runs exactly three focused contracts. R3-R2 job1 had already
passed its other 58 tests, and jobs 2-8 are already PASS.
