Phase 144 R2 Final Repository-Wide Pytest

Purpose
-------
Run the one final canonical repository-wide pytest after Phase 144 Final
Regression Repair R2.

No repository source, existing test, or documentation file is modified by
this package.

Canonical test command
----------------------
python -m pytest tests -q

Environment handling
--------------------
- PYTHONPATH is temporarily set to <repo>;<repo>/tests.
- tests/__init__.py is required by existing package-style test imports.
- If an untracked tests/__init__.py already exists, it is backed up.
- A temporary marker is created only for the run.
- The original untracked marker is restored afterward.
- A tracked marker, if one exists, is left untouched.

Preflight
---------
1. Repository / branch / HEAD / Python / pytest / git status.
2. Dual package import check.
3. Canonical collection-only check for tests/.
4. Exactly one final repository-wide pytest run.

Output
------
- phase144_r2_final_collection.txt
- phase144_r2_final_repository_wide_pytest.log

If the suite fails, do not rerun the whole suite. Use the reported failures
for focused diagnosis and repair.
