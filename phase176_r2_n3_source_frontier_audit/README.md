# Phase 176 R2 — n=3, k=5 Source Frontier Audit

This is a **read-only** Toda source and proof-frontier audit for the unfinished proof of $\pi_8^3$. It does not modify production proof rules, providers, reference registries, renderers, historical tests, or the five primary documents.

Run `run.ps1 -DryRun`, followed by `run.ps1`, from an extracted directory under the existing repository root. The focused tests run without the full test suite. The JSON report is saved to `%LOCALAPPDATA%\EHPProofTracerAudit\phase176_r2_n3_source_frontier_audit\report.json`.

Source anchors: Toda Lemma 5.7, equations (5.2), (5.3), (5.5), Proposition 5.6, Proposition 2.2, and the proof of Proposition 5.9. The chain also depends on the EHP exact sequence (4.4) and Proposition 5.8; those must be inspected before implementing any new general rule.

An anchor match is not a proof certificate. The package records actual proof-search status and possible Web rendering errors separately from source presence. Four historical Phase 174 Source Guard failures remain unresolved and are not executed or reclassified here.
