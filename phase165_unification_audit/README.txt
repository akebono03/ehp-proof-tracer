Phase 165: unified search and dead-route audit (read only)

Extract the ZIP into the repository root and run:

powershell -ExecutionPolicy Bypass -File ".\phase165_unification_audit\run.ps1"

Output files:
phase165_unification_audit_output/report.md
phase165_unification_audit_output/report.json

No production code changes or file deletion. No full pytest. Report identifies legacy references and hard-coded premise sourcing. Confirm runtime reachability and tests before deletion.
