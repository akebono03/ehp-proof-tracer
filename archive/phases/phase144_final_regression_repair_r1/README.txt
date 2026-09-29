Phase 144 Final Regression Repair R1

Confirmed changes only:
- Restore tests/test_phase144_6_pi6_generic_production_route.py to the current develop specification:
  contribution-aware renderer and visible [R1].
- Replace historical fixed inventory totals in R5-37/R5-38/R5-39 tests with structural invariants.

No production files are changed.
No Phase 145 behavior is implemented.
The runner re-runs only the 14 failures observed in the interrupted canonical suite.
It does not run the whole repository suite.

If failures remain, treat them as the next focused repair input.
