# Phase 163 R4-R95: Targeted-Only Closure Audit

This package closes the source-archive registration phase without executing the full pytest suite, as explicitly requested.

It uses the local R91 source catalog, R92 audit, R93 classifier, R94 manifest, and Toda chapter 1–5 TeX files. It independently regenerates the R94 manifest and checks all source hashes, immutable IDs, positions, parent–component links, ambiguous number mappings, bridge references, and non-eligibility for proof search.

All existing project source files, APIs, proof search, and the five root documentation files remain unchanged. The closure report is written to `phase163_r4_r95_output/closure_report.md`; the machine-readable summary is `closure.json`.

Run from the project directory in PowerShell after extracting the ZIP:

```powershell
powershell -ExecutionPolicy Bypass -File ".\phase163_r4_r95_phase_closure\run.ps1"
```

The runner selects four test modules explicitly. It does **not** issue bare `pytest`, nor a repository-wide collection. The results may still reveal existing test problems; no success is declared unless all selected tests and the closure audit succeed. Mathematical certification and original-edition comparison remain deferred to future work.
