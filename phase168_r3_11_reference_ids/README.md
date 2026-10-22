# Phase 168 R3-11 — Registered citation identity

This package augments each `NarrativeCitation` with `reference_ids`, preserving the exact registry reference identifiers associated with the proof steps. It retains the existing locator-based compatibility grouping for duplicate imported registry records and inference-only sources. It does not modify proof search, the default renderer, or Web routes.

Run `run.ps1` from the repository root in Windows PowerShell. It backs up the modified module and runs twelve targeted tests plus a three-goal diagnostic. Full-suite tests are reserved for the end of Phase 168.
