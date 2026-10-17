# Phase 165 R6-2 R4-3: Candidate Provenance Audit

Read-only inspection of R26, Witness R2, Seeded R4, and the shared provider against registered typed goals. No production code is changed, no missing witness is synthesized, and no completed proof is certified.

From the repository root, extract the zip and run `powershell -ExecutionPolicy Bypass -File .\phase165_r6_2_unified_registry_r4_r3\run.ps1`.

Outputs: `reports/provenance.json` and `reports/provenance.md`.

The report does not claim a unique witness was actually used. Exact registry object identity is the only supported rule-ID match; otherwise identity is unresolved. The current GitHub files and `tests/test_phase165_r8_rule_provider.py` were reviewed before implementation.
