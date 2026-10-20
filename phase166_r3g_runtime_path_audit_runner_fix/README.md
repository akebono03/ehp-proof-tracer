# Phase 166 R3-G Runtime Path Audit — Runner Fix

This package fixes only Python module discovery when launching the existing read-only audit from a subdirectory. The audit script is unchanged from the earlier package.

From the repository root, execute `powershell -ExecutionPolicy Bypass -File ".\phase166_r3g_runtime_path_audit_runner_fix\run.ps1"`.

The runner temporarily prepends the repository root to `PYTHONPATH`, restores the previous value afterward, and does not modify production code or run pytest.

The audit saves `phase166_r3g_runtime_path_audit_results.json` in the repository root.
