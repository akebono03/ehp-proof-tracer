# Phase 166 R3-AU-8 — Typed Bridge Boundary Audit

This is a read-only, full-row inspection of the display-element definitions in `data/HyoujiGen.csv` and their ordered uses in `data/sphere.csv`. It records all raw master metadata for each composition factor, without fabricating source/target dimensions or inferring an expression from the optional `generator` reference text.

The current expression model supports `HomotopyElement`, `Composition`, `Sum`, and `Multiple`. Typing remains unverified pending a validated mapping from master metadata to source/target and generator symbols.

Execute `run.ps1` after expanding the package into the repository root. Results are in `results/summary.json` and `results/factor_metadata.csv`. The only tests run are three package-specific pytest tests. Production files are unchanged.
