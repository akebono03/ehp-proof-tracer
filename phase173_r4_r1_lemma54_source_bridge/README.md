# Phase 173 R4-R1: Source-Bound Toda Lemma 5.4 Hopf Bridge

This package experiments with the public proof engine without changing any production files.

It checks the archived Toda Lemma 5.4 against the unchanged Chapter V TeX, checks SHA-256, reuses the original literature reference and its publication position, and registers exactly one typed fixed source claim in a fresh in-memory registry. The source claim is not the Hopf equality itself: an independent inference rule must extract `H(nu_4)=iota_7`. The verified identity is then used in the existing four-premise Toda (5.6) root expansion.

The experiment fails closed if the archived source is missing, not a literal source excerpt, not earlier than the goal, ambiguous, or not citation-screened. It never converts a DB goal, an archive dictionary, or a group presentation into a proof leaf. No files under the tracked production code are modified.

Run from the repository root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r1_lemma54_source_bridge\run.ps1 -DryRun
powershell -NoProfile -ExecutionPolicy Bypass -File .\phase173_r4_r1_lemma54_source_bridge\run.ps1
```

All project tests are deferred until Phase 173 closeout. The focused package tests alone run during this subphase.
