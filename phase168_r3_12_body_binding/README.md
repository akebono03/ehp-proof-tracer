# Phase 168 R3-12 — Proof-step-indexed body citations

Introduces a validated model-backed narrative body boundary. Every renderable line points to an original proof step and receives citations only from `ProofNarrativeModel.step_citation_numbers`. An invalid bidirectional citation mapping raises `ValueError`. No citation inference from rendered mathematics or rule names occurs.

The default long-form Web route is unchanged. The short opt-in renderer now consumes validated body lines. This does not establish a full mathematical narrative; unrenderable conclusions are deliberately skipped rather than fabricated.

Run `run.ps1` in PowerShell from the project root after installing R3-11. Only targeted tests and the four-group search probe run. No full-suite tests run.
