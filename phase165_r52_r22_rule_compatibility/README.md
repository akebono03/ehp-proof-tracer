# Phase 165 R52-R22 — Existing Rule Compatibility Audit

This read-only audit examines five previously implemented inference rule factories for the proof of pi_4^3 and compares their static interfaces with the shared backward-search provider.

Run `run.ps1` from the repository root in PowerShell. This package does not install or modify production files. The resulting `audit_output/compatibility.json` includes the existing factories' complete source and referenced guard and conclusion-builder helpers, while `review.md` summarizes their premise types and direct provider references.

The audit does not prove mathematical correctness, exact goal matching, reference admissibility, or runtime compatibility. No full test suite is run.
