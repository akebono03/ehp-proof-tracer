# Phase 164 R4-R2 — Structured Source Correspondence Audit

This focused, read-only audit compares four typed fields of the existing Proposition 5.1 conclusion and the existing Hopf relation for (5.3) to clauses recorded in the Phase 163 archival manifest. It **does not** establish mathematical equivalence, original-edition verification, or citation eligibility. It does not connect the production search to source-only records.

From the repository root, extract the ZIP there and run:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase164_r4_r2_semantic_structure\run.ps1
```

The runner installs only two new files into the project root / tests directory. It executes targeted pytest files and writes `phase164_r4_r2_output/report.json` and `report.md`. No full pytest is run. Existing registries, inference rules, and renderers remain unchanged.

The report checks source-token presence and the existing typed conclusion's basic shape. Tokens alone do not establish mathematical meaning; a separate, independently reviewed semantic binding is needed to authorize proof usage.
