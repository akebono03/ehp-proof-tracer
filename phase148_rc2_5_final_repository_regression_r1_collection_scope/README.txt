Phase 148 RC2-5 Final Repository Regression R1

Purpose
-------
Repair only the collection scope of the final regression runner.

The previous bare `pytest -q` recursively collected historical archive/ and
phase work-package tests because this repository currently has no pytest
testpaths/norecursedirs configuration. It stopped during collection with
66 errors before the canonical regression suite ran.

Canonical command
-----------------
pytest -q tests

Changes
-------
Production: none
Tests: none
Documentation: none

This package does not change pytest configuration. That would be a repository
test-infrastructure change outside Phase 148 RC2 and is intentionally deferred.

Completion
----------
If the canonical tests/ suite passes, do not rerun it. Return the complete
summary for Phase 148 documentation closure.
