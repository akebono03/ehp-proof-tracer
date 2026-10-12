# Phase 164 R2 — Citation Eligibility Gate

This package adds a narrow, fail-closed citation eligibility check, without modifying existing production modules or the backward proof search. The new module checks migration status, citation origin, caller-supplied independent verification, dependency safety, and the existing Phase 163 R3 publication/availability rule.

## Installation and execution

Extract the ZIP into the repository root, then run from that directory:

```powershell
powershell -ExecutionPolicy Bypass -File .\phase164_r2_citation_eligibility\run.ps1
```

The script installs one new production module and one test file. It fails instead of overwriting a pre-existing R2 module or test. It runs only the four explicitly selected test files; it does not run the full suite.

## Trust boundary

The explicit `verified_assertion_ids` input is a record of independent review supplied by the caller, not a proof of mathematical validity. The module never derives approval from the registry contents. An archival transcript, metadata-only entry, proof-internal assertion, unresolved source, unreviewed dependency, self-reference, circular dependency, or unknown availability cannot become eligible. Existing R3 APIs and results are unchanged.

R3 may consume only results with `usable == True`. R2 does not implement statement matching, ProofStep conversion, search, or narrative generation.
