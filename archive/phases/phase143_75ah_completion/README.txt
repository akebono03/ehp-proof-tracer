Phase 143-75AH completion audit

Implementation focused tests already passed:
30 passed.

This ZIP changes no source files and runs no pytest.

It checks the remaining Narrative rule-name fallback inventory after
TodaLemma57TwoIota5ImageMembershipStatement received semantic rendering.

Expected:
- fallback occurrences: 133 -> 116
- statement types: 22 -> 21
- distinct fallback rule names: 23 -> 22
- target statement: 17 -> 0
- target rule-name fallback: 17 -> 0
- render errors: 0

No full pytest.
