# Phase 176 R3R35 — Composite Suspension Public Provider

This incremental package connects the already isolated, typed Phase 176 R3R34 composite-suspension-equality rule to the common backward proof-search provider. It adds **one** provider call to the nested `expand()` function within `shared_expansion_provider()`. Every candidate retains the independently proved composite `GeneratorImage` as an obligatory premise. It does not add a source assertion, a GIVEN, a new mathematics rule, or a group-specific proof.

## Requirements

Run from the existing `develop` checkout of `akebono03/ehp-proof-tracer` containing Phase 176 R3R34 and R3R31. The installer refuses conflicting edits to the production target, wrong branches, unexpected anchors, and conflicting prior patches. It is idempotent for its own exact prior patch.

## Execution (Windows PowerShell)

Extract this ZIP to the repository root, then run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r35_composite_suspension_public\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase176_r3r35_composite_suspension_public\run.ps1
```

The full replacement text of the modified `shared_expansion_provider()` function, the original production-file backup, and reports are written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r3r35_composite_suspension_public` (the backup is created on the first actual installation only). Inspect `CHANGED_FUNCTION_FULL_JA.md` for the complete function. The production target is modified only on the normal run.

## Scope and proof boundary

The runner executes focused installer, public provider, previous isolated, and existing Hopf tests in separate pytest processes. The entire pytest suite is **not** run. The runtime audit separately reports whether an isolated inference can be replayed, without treating that as a completed, cited shared-search proof. It does not claim the Hopf image or the root group structure is proved. A future phase must inspect the generalized Toda Proposition 2.2 formula for suspended *composite* right factors and equality transport.
