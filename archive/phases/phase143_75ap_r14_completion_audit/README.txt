Phase 143-75AP R14 completion audit

Read-only audit after R13.

Expected completion values:
- scanned groups: 112
- rule-name fallback occurrences: 0
- statement types: 0
- distinct fallback rule names: 0
- render errors: 0

This package does not modify production code and does not run pytest.

If it passes, run the canonical full test suite only once as the final
Phase 143 regression:
  pytest -q ".\tests"
