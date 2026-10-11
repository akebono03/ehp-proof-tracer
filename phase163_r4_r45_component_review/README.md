# Phase 163 R4-R45 — TeX Component Review Packets

This package produces a read-only evidence packet for five priority Toda references: Proposition 5.1, Proposition 5.3, Proposition 5.6, equations (5.1) and (5.3).

From the repository root, run `powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r45_component_review\run.ps1"`.

The script requires existing R4-R42, R4-R43 and R4-R44 outputs, plus the original TeX inputs in the R4-R42 package. It checks source fingerprints, runs only focused tests, and writes `phase163_r4_r45_output/review.json`, `priority_assertions.csv`, and `review.md`.

This is **not** a semantic proof of component-to-text correspondence. No new assertion positions, statement IDs, registry entries, source verification claims, or proof-search connections are made. The remaining assertions are accounted for in `review.json`.
