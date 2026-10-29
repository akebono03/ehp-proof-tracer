# Phase 170 R3-R4 — Fixed-sphere proof generalization audit

This package examines how the **current** proof engine handles a consecutive slice of the groups `pi_(n+k)^n` for **n=2**. It does not change any application code, existing tests, database, Git index or tracked file. It does not install a new proof rule or promote a database row to an inference.

## Scope

- Default: `n=2`, `k=3..10`, including finite cyclic, zero and direct-sum candidates.
- For each group, inspect the explicit `sphere.csv` rows, the existing typed Goal candidates, the source-position resolver, the production backward-search result, open goals and diagnoses.
- For incomplete search results, exercise the same Narrative Model and Web adapter used by the public route; this is **not** an additional complete-proof checker.
- For complete search results only, exercise the actual standard public Web entry and existing Trust Boundary, refusing to mark a case complete if the Web route fails.
- All reports are written to a new directory outside the repository under `%LOCALAPPDATA%\EHPProofTracerRecovery`.

## Invocation

Extract the ZIP into the repository's root and execute `phase170_r3_r4_n2_generalization_audit/run.ps1` using Windows PowerShell. You may pass `-MaxK 12` to extend the finite sample, or `-CaseSeconds 300` for expensive cases. This is an audit of a finite sample, **not** proof of arbitrary-stem completeness.

The script first runs focused tests, then checks the reviewed `develop` ancestry, audited production blob IDs and unchanged database, working tree and Git index. It accepts subsequent Git commits **only** when they added isolated `phase170_` package files, never changed production code.

Outputs include `audit.json` and `audit.md`. `COMPLETE_AND_WEB_VERIFIED` means both the search and the public complete-proof Web path passed. A known DB group with unfinished search is `GOAL_AVAILABLE_PROOF_UNFINISHED`; this is not mathematical impossibility. Any per-case exception or timeout is retained as `CASE_ERROR` and requires review.

The full test suite is not run. No existing documentation files are changed.
