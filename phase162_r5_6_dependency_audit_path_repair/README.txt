Phase 162 R5-6 dependency audit invocation repair.
Run from the repository root after extracting the archive into that root:
  powershell -ExecutionPolicy Bypass -File ".\phase162_r5_6_dependency_audit_path_repair\run_phase162_r5_6_dependency_audit.ps1"

Root cause: executing a script by its subdirectory pathname sets sys.path[0] to that subdirectory, rather than the repository root. This wrapper sets PYTHONPATH to the repository root only for the child process, then restores the original environment.

No production files, tests, or source documents are modified. The audit is read-only. Previously reported 20 focused tests passed, so this patch reruns only the failed audit step. The script contents are unchanged from the earlier ZIP.
