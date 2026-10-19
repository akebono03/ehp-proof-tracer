# Phase 165 R6: Static Dependency Audit

This standalone, read-only audit traces Python import dependencies from collection failures involving a removed group-specific inference rule to an older probe module. It uses Python AST parsing and does not import project modules.

Run `run.ps1` from the project root after the previous triage has created `phase165_r6_audit_results/collection_error_triage.json`.

The report is written to `phase165_r6_audit_results/dependency_chain_audit.json`. Results labeled `UNRESOLVED_STATIC_CHAIN` must not be considered safe to delete, archive, or exclude. This audit changes no production files or tests and does not execute the full pytest suite.
