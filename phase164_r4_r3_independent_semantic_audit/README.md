# Phase 164 R4-R3 — Independent Typed-Clause Audit

This package checks the concrete mathematics represented by the existing two proof leaves against the relevant clauses in the translated Toda TeX archive. It adds only one audit module and one targeted test module; it changes no existing production code, proof search, registry, or renderer.

Run from the repository root:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase164_r4_r3_independent_semantic_audit\run.ps1"
```

Prerequisites: completed Phase 164 R4-R1 and R4-R2 installs, the Phase 163 R94 manifest, Python, and pytest.

Output: `phase164_r4_r3_output/report.json` and `report.md`.

The check is deliberately conservative. A concrete `higher_eta_group_relation` instance is not a proof of the full $n\ge3$ clause. The source-only archive is not mathematically certified. Original-edition verification, citation availability, official typed registry promotion, and proof-search integration remain blocked. Only targeted pytest is run; the full suite is deferred to Phase 164 completion.
