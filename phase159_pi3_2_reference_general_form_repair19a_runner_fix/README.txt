Phase 159 pi3_2 Reference general-form repair19a

Purpose
-------
Fix only the PowerShell runner import path used to verify repair19.

No production Python file is changed by repair19a.

Cause
-----
The repair19 audit script is executed from a child directory.
Python therefore places that child directory at sys.path[0], so modules
located at the repository root such as toda_calculation_facade.py are
not importable.

Fix
---
Temporarily prepend the repository root to PYTHONPATH while the
verification commands run, then restore the previous PYTHONPATH.

Repository-wide pytest is intentionally not run.
