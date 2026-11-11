# Phase 174 R59 — Toda (5.10) Typed Sign Semantics Audit

This is a **read-only audit** of the cited equation (5.10), the typed
`TodaDeltaImageUpToSignStatement`, and the pre-existing general cyclic
kernel inference. There are no production code changes and no new mathematical
proof rules or registered facts.

In the actually cited codomain, the generator has order two. Therefore
its positive and negative values coincide. The printed sign-free equation
and the weaker signed typed witness have the same effect **in this checked
context**, not for an arbitrary codomain.

From the repository root, run `run.ps1 -DryRun` and then `run.ps1`.
The script performs pinned source verification, an independent structural
consistency check, the existing R57 two-group public proof audit, and focused
pytest only. It does not run the whole test suite.

The audit result is written outside the working tree beneath
`%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r59_toda510_signed_semantics_audit`.

A future migration to an exact-equality statement type would need an explicit
consumer impact review and a backward-compatible bridge. R59 deliberately
does not change the meaning of the common inference engine.
