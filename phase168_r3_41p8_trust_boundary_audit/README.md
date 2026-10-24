# Phase 168 R3-41P8 — ProofStep Trust Boundary Audit

This audit is read-only. It does not patch the application, test suite, registries, or database.

It compares three public group-proof texts and their citations against the R3-41P7 captured outputs. It also constructs artificial, invalid `ProofStep` graphs that carry syntactically plausible typing, provenance, and inference rule metadata. Those artificial examples are probes, not mathematical facts.

The purpose is to establish whether eliminating runtime shape validation before defining a trusted proof boundary could allow incorrect mathematical sentences to appear. All real proof inference validation remains in the backward-search rules.

Run `run.ps1` from an extracted package placed directly in the repository root. The script executes a focused pytest subset and creates `output/review_bundle.zip`. The full pytest suite is not run.
