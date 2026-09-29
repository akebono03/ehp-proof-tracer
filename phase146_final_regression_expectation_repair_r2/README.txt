Phase 146 Final Regression Expectation Repair R2

Changes:
- Production code: none.
- Existing tests: one remaining stale pi6 group-structure purpose expectation.
- Restores CRLF in the five files touched by R1 so git diff reflects semantic
  changes rather than whole-file line-ending churn.

R2 intentionally does not implement Phase 147 behavior.

After focused PASS and a small git diff:
  python -m pytest tests -q --durations=50
