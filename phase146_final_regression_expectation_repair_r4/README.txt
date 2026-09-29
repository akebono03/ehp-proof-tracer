Phase 146 Final Regression Expectation Repair R4

R4 fixes the R3 harness issue: local HEAD test files use mixed LF/CRLF line
endings, so R3's LF-only byte patterns stopped after the first file.

R4:
- restores all five affected tests from HEAD;
- detects each file's existing newline convention;
- preserves that convention;
- applies only the Phase 146-7 expectation changes;
- aborts immediately on any failed step;
- runs the 31 focused tests;
- verifies and prints the exact minimal diff.

Production code changes: none.
No Phase 147 functionality is implemented.

After PASS:
  python -m pytest tests -q --durations=50
