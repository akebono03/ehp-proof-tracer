Phase 159 R1-7c R4 exact-sequence subsequence suppression audit2 fix1

Purpose
-------
Fix only the audit-script import path.

Cause
-----
The audit Python file lives in a subdirectory. Running that file directly
made Python use the audit directory as sys.path[0], so repository-root modules
such as toda_calculation_facade could not be imported.

Fix
---
Add the repository root to sys.path before importing project modules.

Production code changes: none.
Test code changes: none.
No full pytest.
