# Phase 166 R3-AO Semantic Type Audit

This is a read-only audit. It inspects 112 database-derived group goals, including generator source/target dimensions, composition interfaces, stable and direct `Element` ID stems, and group component orders. It does not modify production code, search for proofs, or run the full pytest suite.

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase166_r3ao_semantic_type_audit\run.ps1
```

Results are written to `results/report.json` and `results/report.md`. Simple generator goals are `partially_verified` even when their ambient dimensions agree: this audit does not establish equivalence between a string-only generator name and its ID decomposition.
