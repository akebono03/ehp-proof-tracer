# Phase 165 R6 — pi32 test migration

This patch replaces two complete test functions in `tests/test_phase49_probe.py` with checks against the current shared typed Backward Search for pi32. No production files, legacy probe implementations, or other tests are changed. The installer backs up the test file before rewriting it, guards against an unexpected original body, and runs three targeted tests. This does not establish coverage equivalence for the other historical tests.
