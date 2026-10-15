# Phase 165 R57-R24 — Typed Candidate Discovery

This package adds read-only inference-rule candidate discovery without changing production search, the rule registry, or any group-specific adapter. It builds on the R23-R1 conclusion-unification module already installed at repository root. `run.ps1` copies only the new R24 module into the repository and runs the R24 targeted tests. It does not run the full test suite.

The implementation reuses the existing `InferenceRuleCatalog` and its safety/compatibility filters and the R8 inspected rule-factory discovery. An explicit `conclusion_pattern` is required. Candidates are not proofs, and no premises are constructed. R25 is responsible for premise generation; R26 is responsible for recursive-search integration. Opaque `conclusion_builder` rules remain outside the reverse-matching contract.
