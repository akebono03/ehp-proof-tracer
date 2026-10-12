# Phase 163 R4-R59 — Isolated ID and publication-order trial

This read-only trial uses R4-R58 archival readiness records. It demonstrates that identifiers and publication positions are separate fields, and that a synthetic insertion can change positions without changing existing IDs. A second synthetic insertion illustrates component ordering within one reference. No synthetic item represents a Toda statement.

Run `run.ps1` from PowerShell after extracting the ZIP into the project root. The input must exist at `phase163_r4_r58_output/readiness.json`. Requires Python and pytest, and imports the existing `unified_statement_registry.py` from the project. Outputs are written to `phase163_r4_r59_output`.

Only the focused tests are run. Production registry, existing IDs, proof search and Toda TeX are not modified. No mathematical equivalence or source-edition verification is claimed.
