Phase 155-R3-3B — deletion-candidate file/dependency safety audit

Purpose
-------
Audit the 161 R3-3A deletion-candidate test functions before any source file
is modified.

The audit separates two questions:

1. Can the candidate test FUNCTION be removed?
2. Can the entire test FILE be removed?

Function safety
---------------
A candidate test function is blocked when another Python module imports or
references that test function directly.

A candidate function can still be safe even when its file contains retained
tests or externally imported helper functions.

File safety
-----------
A whole test file is eligible for deletion only when:

- every top-level `test_*` function in the file is an R3-3A deletion
  candidate,
- no other Python module imports the whole test module,
- no other Python module imports any symbol from that test module.

This deliberately protects helper-provider test modules such as the current
repository pattern:

`from tests.test_phase143_19_method_evidence import _method_evidence_data`

Files containing retained tests are function-only deletion targets.

What is recorded
----------------
Per candidate:
- function existence,
- direct external function references,
- retained tests in the same file,
- helper count,
- constant count,
- import count,
- external symbol imports,
- whole-module imports,
- recommended deletion action.

Per file:
- all top-level tests,
- deletion-candidate tests,
- retained tests,
- helpers,
- classes,
- constants,
- imports,
- external symbol imports,
- whole-module imports,
- whole-file deletion eligibility.

Boundary
--------
- production changes: none
- existing-test changes: none
- deleted tests: 0
- repository-wide pytest: not run

R3-3C may delete only the functions/files that R3-3B marks safe.
