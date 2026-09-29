Phase 143 final regression R2

The first final-regression command used bare `pytest -q`.
The local repository contains many extracted Phase 143 work-package
directories with duplicate copies of test modules. Pytest recursively
collected those copies and stopped during collection with import-file
mismatch errors. That run did not execute the canonical regression suite.

R2 makes no production-code or test changes.

It runs only the canonical repository test directory:
pytest -q .\tests

This prevents extracted phase143_* work-package directories from being
mistaken for canonical tests.

If this passes, combine it with the already-passed completion audit:
- 112 groups
- 11033 presentation nodes
- 0 rule-name fallbacks
- 0 unhandled statement types
- 0 fallback rule names
- 0 render errors

No files are deleted or modified by this package.
