# Phase 176 R3R2 — Finite-Cyclic Hopf Frontier Audit

This package performs a read-only audit of the missing finite-cyclic generator derivation for the registered `(n,k)=(3,5)` group. It inspects the actual proof search, typed map-property goals, source metadata, and proposals from the shared backward provider. Proposals are not certificates or newly introduced proofs.

Extract this ZIP into the EHP Proof Tracer repository root on the `develop` branch. Run `run.ps1 -DryRun` and then `run.ps1`. Both paths preserve existing source files. The normal run executes **focused tests only** and writes a JSON report outside the repository. It never runs the full test suite, commits code, resets the tree, or changes source assertions.

The original Phase 174 historical source-guard failures remain unresolved. See `AUDIT_PLAN_JA.md` and `CODE_FULL_JA.md` for the exact scope and complete new code.
