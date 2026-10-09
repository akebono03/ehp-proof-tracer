Phase 162 R8 — PowerShell quoting repair

Only run.ps1 is changed. No Python source or tests are changed.
The repository-root module was already installed by the previous package.
The previous python -c import check is removed because its quoted Python
string is mangled by Windows PowerShell argument passing. The existing
module-install regression test verifies the import and source path.

Place this folder under the EHP Proof Tracer repository root. Execute:
  powershell -ExecutionPolicy Bypass -File ".\phase162_r8_runner_quote_fix\run.ps1"

Expected: 4 focused tests. Full test suite not run.
