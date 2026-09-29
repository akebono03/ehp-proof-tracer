Phase 144 Repository-Wide Pytest R1

Purpose
-------
Run the single final canonical repository-wide pytest for Phase 144.

Canonical command
-----------------
python -m pytest tests -q

Why R1 is required
------------------
The first runner used `python -m pytest -q`, which recursively collected old
Phase work/audit package tests outside the canonical `tests/` directory and
stopped during collection.

A subsequent direct `python -m pytest tests -q` lacked the import environment
required by the current canonical test suite and also stopped during collection.

R1 combines the two required conditions:
1. Collect only the canonical `tests/` directory.
2. Support both package-style (`tests.<module>`) and top-level test-module
   imports by:
   - temporarily creating `tests/__init__.py` only when absent;
   - setting PYTHONPATH to repository root + repository root/tests;
   - removing the temporary marker in `finally`.

Changed file
------------
phase144_repository_wide_pytest_r1/run_phase144_repository_wide_pytest_r1.ps1

Production changes: none.
Existing test changes: none.
Documentation changes: none.
Phase 145 implementation: none.

Completion
----------
If the canonical test suite passes, do not run another repository-wide pytest
for Phase 144. Record the actual passed-count and elapsed time and proceed to
Phase 144 documentation/finalization.
