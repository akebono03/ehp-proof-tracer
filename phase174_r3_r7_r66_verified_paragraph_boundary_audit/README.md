# Phase 174 R66 — Verified Paragraph Boundary Audit

This read-only audit reuses the existing certified Group proof search for `n=6,k=5` and `n=7,k=5`, and the R63–R65 citation coverage and candidate evidence. It checks the full 15-paragraph outstanding frontier, without asserting sentence-level mathematical correctness.

- For the two paragraphs with no literal typed-statement projection, it attempts exact matching to EHP exactness-chain text produced from certified windows.
- For the seven uncited candidate statements, it verifies original ProofStep identity and recorded provenance without inserting a citation.
- For the six cited candidates, it verifies each source label belongs to a real GIVEN ancestor, not merely to the whole model.

No source assertion, new GIVEN, inference rule, proof tree, renderer, existing test, or production file is modified. The source guard checks reviewed Git blob SHA values; new unrelated commits do not invalidate the audit. The run script disables pytest's cache provider and does not run the full suite.

Run `powershell -NoProfile -ExecutionPolicy Bypass -File .\phase174_r3_r7_r66_verified_paragraph_boundary_audit\run.ps1 -DryRun`, then run the same command without `-DryRun`. Results are written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r66_verified_paragraph_boundary_audit\`.
