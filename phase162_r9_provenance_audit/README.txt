Phase 162 R9: read-only provenance audit

No production modules are modified. Full suite is not run.

Run from the repository root after extracting the ZIP there:

powershell -ExecutionPolicy Bypass -File ".\phase162_r9_provenance_audit\run.ps1"

Outputs:
  phase162_r9_provenance_audit/audit_output/provenance.md
  phase162_r9_provenance_audit/audit_output/provenance.json
  phase162_r9_provenance_audit/audit_output/narrative.md

The report identifies direct proof dependencies, all ancestor nodes, text
fragments, and the origin of appended stable transport prose. This is a
structural audit, not a mathematical proof validation.
