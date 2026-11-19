# Phase 175 R4R12R13R1 — Delta Injectivity Frontier Audit

This is a **read-only audit**, not a patch to EHP Proof Tracer's proof search. It inspects the checked Toda (5.8) equation, both typed Proposition 4.2 exactness windows and current public backward expansion candidates for the appropriate Delta-injective and suspension-surjective goals.

Run `run.ps1 -DryRun` and `run.ps1` after extracting at the repository root, on branch `develop`. Both modes are read-only. A passing gate is not a complete proof, a proof certificate, or evidence that the recursive search has succeeded. It does not register new rules, literature assertions or a direct group conclusion.

The script creates `output/report.json` within this package. It runs only three focused pytest cases and never the full test suite.
