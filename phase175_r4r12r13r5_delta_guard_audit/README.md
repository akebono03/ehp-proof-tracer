# Phase 175 R4R12R13R5 — Delta Typed Guard Audit

This package performs a read-only audit of the existing, conditional Toda (5.8) Delta injectivity candidate. It compares the cited expression's canonical generator objects to the actual earlier database group presentation and checks whether the shared provider emits a proposal.

It does not alter production code, add mathematical rules, add GIVENs, or claim a completed proof. The audit explicitly distinguishes citation screening, group shape, each generator's exact equality, free-coordinate calculation, rule acceptance, and shared-provider availability.

Run from the repository root with `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase175_r4r12r13r5_delta_guard_audit\run.ps1 -DryRun`, then without `-DryRun`.

Only three focused tests are executed. Full pytest is reserved for the end of Phase 175.
