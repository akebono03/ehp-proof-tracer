Phase 165 R27-R12 -- READ ONLY

Targets:
- standard_production_repository.py::build_standard_production_proof_repository
- standard_repository.py::build_standard_proof_repository
- proof_repository.py::ProofRepository and ProofRepositoryEntry
- toda_prop515_upper_bootstrap.py::build_toda_prop515_upper_bootstrap
- downstream live usages, generic typed-registry dependencies and relevant test references

No production files are modified. No deletion authorized. This audit scans function-level AST symbol references across Python files; it does not prove that every dynamic invocation has been detected. Review audit_report.json before any removal.

Run from repository root: powershell -ExecutionPolicy Bypass -File .\phase165_r27_r12\run.ps1
