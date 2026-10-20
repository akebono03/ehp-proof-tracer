# Phase 166 R3-G route audit: Python import path repair

This patch changes **only the invocation** of the read-only audit. Running `python -m phase166_r3g_route_check_path_fix.audit` from the repository root includes the repository root in Python's module search path. It does not alter any project source files or tests.

The earlier `list + tuple` correction is retained in the complete `audit.py`.

Unzip in the project root and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase166_r3g_route_check_path_fix\run.ps1
```

Audit output: `phase166_r3g_route_check_path_fix/audit_result.json`. Full pytest is not run.
