# Phase 165 R27-R22-R1 installer repair

This patch fixes the overly strict import-layout matching of the previous R27-R22 installer. It updates only `web_group_query.py`, with an AST-validated replacement of `build_standard_web_group_query_view`, preserving unrelated code and creating a backup. It does not run the full test suite.

From the repository root, extract the ZIP and execute `powershell -ExecutionPolicy Bypass -File .\phase165_r27_r22_r1_import_fix\run.ps1`.
