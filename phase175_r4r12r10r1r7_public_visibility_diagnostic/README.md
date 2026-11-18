# Phase 175 R4R12R10R1R7 — Public Visibility Diagnostic

This is a read-only investigation following an R10R1 DryRun PASS and an execution failure with `R10R1_CITED_511_NOT_PUBLIC`. It does **not** reinstall or modify the shared provider, sources, rules, or previous tests. It records the precise number of citation-bearing source links and proposals available at each layer.

Unzip into the `develop` checkout and run `run.ps1 -DryRun` followed by `run.ps1`. The generated JSON under `output/` distinguishes a missing citation, a screened-out citation, a public wiring issue, or duplicate candidates. This package does not claim that the EHP quotient proof is complete. Full-suite pytest is intentionally not run.

The previously failed R10R1 installer may already have modified `phase165_r52_r9_shared_math.py`; this package deliberately does not undo or repeat that installation.
