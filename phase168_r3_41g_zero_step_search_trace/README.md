# Phase 168 R3-41G — Read-Only Search Trace

This audit observes the canonical typed backward-search engine without modifying its proof rules, search results, public web routes, or renderer. It distinguishes missing root expansion candidates from unresolved premises of existing expansion candidates and preserves the original progress observer.

Run `run.ps1` from the extracted package folder under the repository root. The runner executes only relevant focused pytest cases and then the live audit. Outputs are written to `output/audit.json`, `output/audit.md`, and `output/review_bundle.zip`.

A root expansion is a candidate, not a proof. The tracer never supplies missing ProofSteps or inferred literature references. This package does not run the full test suite.
