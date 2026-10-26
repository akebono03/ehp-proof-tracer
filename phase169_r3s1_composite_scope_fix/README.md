# Phase 169 R3S1 — Composite Source Scope Repair

A focused corrective patch for the R3S citation projection regression. Registered
atomic child assertions inherit their parent compound scope. The original R3S
renderer mistakenly expected each child to hold the entire parent structure.

The patch recognizes a declared parent composite and verifies atomic children
against their actual recorded parent and typed field. No facts, references,
proof steps, search algorithms, or other renderers are changed.

Run `run.ps1` after extracting the archive into the repository root.
It runs only relevant pytest selections and restores the production file on failure.
Full pytest is intentionally not run during this phase.
