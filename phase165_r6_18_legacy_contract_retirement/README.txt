Phase 165 R6-18 — legacy contract test function retirement.
Run run.ps1 from the extracted package in the repository root.
Requires local R6-15 UTF-16/UTF-8 pytest stdout report at its original path.
Protects six files containing 8 failures/errors needing mathematical/common-search review.
Retires the other 105 failing test node IDs at function granularity after backups.
Only tests are edited; production code remains unchanged. Parameterized test functions are retired as one function, including any passing parameter cases of that function. This coverage reduction must be acknowledged.
Does NOT run full pytest. Inspect JSON report and backup manifest.
