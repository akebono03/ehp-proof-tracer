# Phase 166 R2 — Toda (5.3) Correspondence Audit

This is a read-only, fail-closed inspection of the four source rows attributed to Toda (5.3). It compares the display fields with the registered fixed-statement *component metadata* and records duplicate display signatures. It does not construct a typed `Relation`, certify mathematical identity, grant citation eligibility, or change any production file.

Place this folder at the root of the existing EHP Proof Tracer checkout, with `sphere_relation2.csv` present at the root or inside `phase166_r1_source_registry_audit/`. Run `powershell -ExecutionPolicy Bypass -File .\phase166_r2_equation53_audit\run.ps1` from the repository root. Requires Python and pytest and the current project modules. Results appear in `results/equation53_rows.csv` and `results/summary.json`.

Targeted pytest is used; the full test suite must run only in Phase 166 R10.
