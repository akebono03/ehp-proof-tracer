Phase 155 Closure-R2B-R4 — final historical-heavy cleanup

Final partition of the remaining 14 audit-only nodeids:
- DELETE: 10
- LIGHTWEIGHT_REPLACE: 2
- KEEP_AUDIT_ONLY: 2

The installer validates the exact 14-nodeid boundary before editing anything.

The two retained audit-only tests are:
1. test_phase144_6_r5_43_11d_final_completion_invariants_pass
2. test_phase144_6_r5_43_11d_renderer_remains_generic

No heavy audit is executed in R2B-R4.
No repository-wide pytest is executed.
No production code is changed.
