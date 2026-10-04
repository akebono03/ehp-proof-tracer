Phase157-R20 repair9 fixed1

Purpose
-------
Fix only the import-path defect in the repair9 audit launcher.

Cause
-----
The audit Python file is executed from a subdirectory, so Python places that
subdirectory at sys.path[0]. Repository-root modules such as
`toda_calculation_facade.py` are therefore not importable by default.

Fix
---
The PowerShell launcher sets PYTHONPATH to the current repository root before
running the unchanged audit logic.

Production code changes: none.
Test changes: none.
Documentation changes: none.
pytest: not run.
