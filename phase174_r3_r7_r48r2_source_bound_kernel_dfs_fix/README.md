# Phase 174 R3-R7-R48R2 — Source-Bound Kernel DFS Repair

This guarded package updates only R48's read-only audit and one static regression test. The unmodified R35 general cyclic kernel rule requires an inferred free-cyclic domain. Typed-reference search previously selected a direct GIVEN for that same concrete domain, so the kernel rule did not match. This audit-only repair uses the existing `SourceBoundGoal` search obligation to require a genuine cited specialization. It does not create a new mathematical rule, register a GIVEN, inject a ProofStep, or change production files.

Run `run.ps1 -DryRun`, then `run.ps1`. The runner executes R48's focused audit and focused regressions; no full pytest suite is invoked.
