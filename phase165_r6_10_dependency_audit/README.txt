Phase 165 R6-10 — dependency audit (read-only)

Extract this folder into the repository root, then run:

cd C:\Users\oomae\Dropbox\Python\fitz\ehp_proof
Expand-Archive -Path "$HOME\Downloads\phase165_r6_10_dependency_audit.zip" -DestinationPath "." -Force
powershell -ExecutionPolicy Bypass -File ".\phase165_r6_10_dependency_audit\run.ps1"

Outputs:
phase165_r6_audit_results\r6_10_dependency_audit\report.json
phase165_r6_audit_results\r6_10_dependency_audit\report.md

No existing source, test, Probe, or mathematical definition is altered.
This scan inspects Python import and direct builder call edges in repository-root Python modules, tests, and probes. It does not prove absence of dynamic imports, CLI references, or dependencies in historical scripts. Review its results before R6-11 retirement.
