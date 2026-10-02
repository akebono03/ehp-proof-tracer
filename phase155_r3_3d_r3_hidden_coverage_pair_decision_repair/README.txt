Phase 155-R3-3D-r3 — hidden coverage preservation / pair decision repair

Purpose
-------
This subphase still performs audit only.

For the eight divergent same-name test groups, it checks every assertion that
exists only in a shadowed earlier definition against all current
`tests/test_*.py` runtime definitions.

A shadowed group is classified as cleanup-ready only when:
- it has no hidden-only assertions, or
- every hidden-only assertion is already exercised by another runtime test.

Otherwise the hidden coverage must be preserved before cleanup.

For the two unresolved removable pairs, it reconstructs the current semantics
of the older/newer tests, checks assertion/call containment, checks external
references to the older test function name, and combines this with the
R3-2F-r1 verified `removable_duplicate` decision.

The output is a repaired decision plan only. No tests are edited or deleted.

Repository-wide pytest is NOT run.
