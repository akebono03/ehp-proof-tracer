# EHP Proof Tracer Phase 174 — R65

R65 is a **read-only** inventory and candidate provenance audit for the remaining 15 proof paragraphs from R64.

It replays the established, verified Group queries, matches only literal typed-sentence or LaTeX projections, and records whether displayed source numbers belong to GIVEN ancestors of candidate proof steps. It never treats a text match as mathematical sentence-level certification.

The report is written to `%LOCALAPPDATA%\EHPProofTracerAudit\phase174_r3_r7_r65_paragraph_provenance_candidate_audit\report.json` and `frontier.md`.

Extract the ZIP into the project root. Run `run.ps1 -DryRun` and then `run.ps1`. Only focused pytest is used; no full project test suite runs.
