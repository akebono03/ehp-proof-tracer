Phase 143-75AG R5 + completion audit

R4 result:
- 36 tests passed
- one test failed only because the expected string used a shortened
  Delta iota notation
- the existing generic expression renderer canonically emits
  Delta\left(iota\right)

R5 production changes:
- none

R5 test change:
- update the exact expected string to the existing canonical
  MapApplication rendering

Then run the remaining-fallback completion audit.

Expected completion:
- fallback occurrences: 152 -> 133
- statement types: 23 -> 22
- distinct fallback rule names: 24 -> 23
- target statement: 19 -> 0
- render errors: 0

No full pytest.
