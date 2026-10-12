# Phase 163 R4-R56 — Explicit Scope Evidence Trial

This isolated, read-only audit extracts only the source-explicit variables, map domain/codomain, and piecewise conditions for Toda equations (2.9), (2.10), and (4.3). It is not a formal mathematical parser.

Run `run.ps1` from the repository root after extracting this package. The runner needs `phase163_r4_r47_output/catalog.json`, `phase163_r4_r55_output/trial.json`, Python, and pytest. Results are written to `phase163_r4_r56_output/` as `scope.json`, `scope.csv`, and `report.md`.

No production Registry, source TeX, existing API, proof search, or Statement ID is modified. Only nine targeted tests run; the full suite remains reserved for Phase closure.
