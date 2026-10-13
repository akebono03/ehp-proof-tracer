Phase 165 R49 structural audit (runner encoding fix)

Extract into the repository root, overwriting the previous audit folder.

powershell -ExecutionPolicy Bypass -File ".\phase165_r49_structural_audit\run.ps1"

Outputs:
phase165_r49_audit_output/report.md
phase165_r49_audit_output/report.json

This is a read-only structural audit. No production files modified; pytest not run.
The runner deliberately contains ASCII-only characters to support Windows PowerShell 5.1.
