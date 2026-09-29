Phase 144 Repository-Wide Pytest

Purpose
-------
This package performs the single final repository-wide pytest run for Phase 144.

Command
-------
python -m pytest -q

Environment compatibility
-------------------------
The current test tree uses both package-style imports (`tests.<module>`) and
top-level imports from the tests directory. The runner therefore:
- sets PYTHONPATH to repository root + repository root/tests;
- creates tests/__init__.py temporarily only when it is absent;
- removes that temporary marker in finally.

Changes
-------
Production changes: none
Test changes: none
Documentation changes: none

After PASS, use the actual passed-count and elapsed time from this run when
finalizing the Phase 144 documentation. Do not run another repository-wide
pytest for Phase 144.
